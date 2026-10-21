"""Exercise public prompt templates and token alignment without private runs or model downloads."""
import json
import unittest

from tokenizers import Tokenizer, models, pre_tokenizers, decoders
from transformers import PreTrainedTokenizerFast

from axis_rh.codebench import harness
from axis_rh.correlation.rh_hillclimb import conversation_before_turn, WorklistSettings
from axis_rh.correlation.transcripts import tokenize_transcript, transcript_token_indices_by_region
from axis_rh.correlation.generate import generated_token_offsets


class TranscriptInputTests(unittest.TestCase):
    def test_workspace_templates_and_feedback(self):
        for scenario, is_function in [("evilgenie", True), ("evilgenie", False), ("evilgenie_lcbpro", False)]:
            with self.subTest(scenario=scenario, is_function=is_function):
                example = dict(kind="workspace", scenario=scenario, example_id="synthetic",
                               title="Echo", description="Return the input.", is_function=is_function,
                               function_name="echo" if is_function else None,
                               starter_code="def echo(x):\n    return x\n",
                               visible_tests=[dict(input="1", output="1")], holdout_tests=[])
                files = harness.workspace_files(example)
                self.assertEqual(set(files), {"problem.md", "solution.py", "test_cases.json", "test.py"})
                self.assertEqual(json.loads(files["test_cases.json"])[0]["input"], "1")
                for name in ("solution.py", "test.py"):
                    self.assertNotIn("{{", files[name])
                    compile(files[name], name, "exec")  # Parse only; never execute generated code.
                record = dict(feedback="neutral", max_attempts=3, attempt_budget_stated=True,
                              attempts=[dict(completion="No file blocks.", stdout="", stderr="", wrote=False),
                                        dict(completion="Final answer only.", stdout="failed", stderr="", wrote=True)])
                messages = conversation_before_turn(example, record, WorklistSettings({}, "System"), 2)
                self.assertEqual([m["role"] for m in messages], ["system", "user", "assistant", "user", "assistant", "user"])
                self.assertIn(files["test.py"], messages[1]["content"])
                self.assertIn("no file blocks", messages[3]["content"])
                self.assertIn("2 of 3 submissions remaining", messages[3]["content"])
                self.assertEqual(messages[4]["content"], "Final answer only.")
                self.assertIn("failed", messages[5]["content"])
                self.assertIn("1 of 3 submissions remaining", messages[5]["content"])

    def test_check_prompt_and_error_reconstruction(self):
        example = dict(kind="check", prompt="def echo(x): pass", test="def check(f): assert f(1) == 1", entry_point="echo")
        record = dict(feedback="neutral", max_attempts=2, attempt_budget_stated=True,
                      attempts=[dict(completion="def echo(x): return 0", stdout="ignored", stderr="AssertionError")])
        messages = conversation_before_turn(example, record, WorklistSettings({}, None), 1)
        self.assertIn("Use check(echo)", messages[0]["content"])
        self.assertIn("AssertionError", messages[-1]["content"])
        self.assertNotIn("ignored", messages[-1]["content"])

    def test_byte_tokenizer_alignment_preserves_utf8_and_excludes_role_markers(self):
        vocab = {token: i for i, token in enumerate(["<user>", "<assistant>", *sorted(pre_tokenizers.ByteLevel.alphabet())])}
        backend = Tokenizer(models.BPE(vocab, merges=[]))
        backend.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
        backend.decoder = decoders.ByteLevel()
        tokenizer = PreTrainedTokenizerFast(tokenizer_object=backend, additional_special_tokens=["<user>", "<assistant>"])
        tokenizer.chat_template = "{% for m in messages %}<{{ m['role'] }}>{{ m['content'] | trim }}{% endfor %}{% if add_generation_prompt %}<assistant>{% endif %}"
        messages = [{"role": "user", "content": " café "}]
        transcript = dict(messages=messages, chat_kwargs={}, raw_response="é!")
        tokenized = tokenize_transcript(tokenizer, transcript)
        self.assertEqual(tokenized.prompt, "<user>café<assistant>")
        self.assertEqual(tokenizer.decode(tokenized.response_ids), "é!")
        # The split UTF-8 bytes cannot be decoded independently: exercise exact-ID fallback.
        self.assertNotEqual("".join(tokenizer.decode([i]) for i in tokenized.response_ids), "é!")
        self.assertIsNotNone(generated_token_offsets(tokenizer, tokenized.response_ids, "é!"))
        self.assertIsNone(generated_token_offsets(tokenizer, tokenized.response_ids[:-1], "é!"))
        regions, alignment = transcript_token_indices_by_region(
            tokenizer, messages, "é!", tokenized, dict(cot=[], final=[(0, 2)]))
        self.assertEqual(alignment, "exact")
        self.assertEqual(tokenizer.decode([tokenized.prompt_ids[i] for i in regions["prompt"]]), "café")
        self.assertEqual(regions["cot"], [])
        self.assertEqual(regions["final"], list(range(len(tokenized.prompt_ids), len(tokenized.prompt_ids) + len(tokenized.response_ids))))


if __name__ == "__main__":
    unittest.main()
