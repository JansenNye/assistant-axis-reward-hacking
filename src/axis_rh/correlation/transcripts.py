"""Teacher-forced transcript tokenization and exact region alignment."""
from __future__ import annotations
from typing import Literal, NamedTuple
from axis_rh.common.chat import Conversation
from transformers import PreTrainedTokenizerBase
from axis_rh.measurement.templates import ResponseSpans
from .generate import last_message_token_indices, response_token_indices_by_region
from .records import Region, TranscriptRecord
Alignment = Literal["exact", "unavailable"]

class TokenizedTranscript(NamedTuple):
    prompt: str
    prompt_ids: list[int]
    prompt_offsets: list[tuple[int, int]]
    response_ids: list[int]


def tokenize_transcript(tokenizer: PreTrainedTokenizerBase, transcript: TranscriptRecord) -> TokenizedTranscript:
    prompt = tokenizer.apply_chat_template(
        transcript["messages"], add_generation_prompt=True, tokenize=False, **transcript["chat_kwargs"])
    prompt_encoding = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    response_ids: list[int] = tokenizer(transcript["raw_response"], add_special_tokens=False)["input_ids"]
    return TokenizedTranscript(prompt, prompt_encoding["input_ids"], prompt_encoding["offset_mapping"], response_ids)


def transcript_token_indices_by_region(tokenizer: PreTrainedTokenizerBase, messages: Conversation, raw_response: str,
                                       tokenized: TokenizedTranscript,
                                       spans: ResponseSpans) -> tuple[dict[Region, list[int]], Alignment]:
    prompt_indices = last_message_token_indices(
        tokenizer, messages, tokenized.prompt, tokenized.prompt_offsets, tokenized.prompt_ids)
    response_indices_by_region = response_token_indices_by_region(
        tokenizer, tokenized.response_ids, raw_response, spans, len(tokenized.prompt_ids))
    if response_indices_by_region is None:
        return {"prompt": prompt_indices}, "unavailable"
    return {"prompt": prompt_indices, **response_indices_by_region}, "exact"
