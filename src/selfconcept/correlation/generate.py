"""Token alignment helpers extracted unchanged from the experiment runner."""
from __future__ import annotations
from itertools import accumulate
from selfconcept.common.hf_strong_types import configure_call, Conversation, HFTokenizer, OffsetMappingPresent
from selfconcept.measurement.templates import content_token_indices, ResponseSpans
from .records import Region

def generated_token_offsets(tokenizer: HFTokenizer, token_ids: list[int], text: str) -> OffsetMappingPresent | None:
    # Single-token decoding is exact for ordinary text, but not split UTF-8.
    pieces = [tokenizer.decode([token_id], skip_special_tokens=False, clean_up_tokenization_spaces=False)
              for token_id in token_ids]
    if "".join(pieces) == text:
        ends = list(accumulate(len(piece) for piece in pieces))
        return list(zip([0] + ends[:-1], ends))
    encoding = configure_call(tokenizer).return_offsets_mapping(True)(text, add_special_tokens=False)
    if encoding["input_ids"] == token_ids:
        return encoding["offset_mapping"]
    return None


def check_context_budget(model: PreTrainedModel, prompt_length: int, max_new_tokens: int) -> None:
    context_limit = getattr(getattr(model.config, "text_config", model.config), "max_position_embeddings", None)
    if context_limit and prompt_length + max_new_tokens > context_limit:
        raise ValueError("Prompt plus generation budget exceeds model context; refusing silent truncation")


def last_message_token_indices(tokenizer: HFTokenizer, messages: Conversation, prompt: str,
                               prompt_offsets: OffsetMappingPresent, prompt_ids: list[int]) -> list[int]:
    # Measure only content from the last externally supplied message, excluding
    # assistant history, system instructions and generation-role delimiters.
    # Native templates may trim user content (notably coding feedback's
    # leading newline). Match the shared non-whitespace content exactly.
    last_message = messages[-1]["content"].strip()
    start = prompt.rfind(last_message)
    if start < 0:
        raise ValueError("Cannot exactly locate the last message in the rendered prompt")
    return content_token_indices(prompt_offsets, [(start, start + len(last_message))], tokenizer.all_special_ids, prompt_ids)


def response_token_indices_by_region(tokenizer: HFTokenizer, new_token_ids: list[int], raw_response: str,
                                     spans: ResponseSpans, prompt_length: int) -> dict[Region, list[int]] | None:
    offsets = generated_token_offsets(tokenizer, new_token_ids, raw_response)
    if offsets is None:
        return None
    return {region: [prompt_length + index
                     for index in content_token_indices(offsets, spans[region], tokenizer.all_special_ids, new_token_ids)]
            for region in ("cot", "final")}
