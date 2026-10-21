import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


type ReasoningByExampleTurn = dict[tuple[str, int], str]


class ModelSpecifics(Protocol):
    def split_attempt(self, example_id: str, turn: int, completion: str) -> tuple[str, str]:
        """-> (reasoning, content) of the example's attempt at 0-based turn."""
        ...


@dataclass(frozen=True)
class HarmonyModelSpecifics:
    """GPT-OSS: the completion is the final channel only, and the analysis
    channel is in the run's reasoning sidecar."""

    reasoning_by_example_turn: ReasoningByExampleTurn

    def split_attempt(self, example_id: str, turn: int, completion: str) -> tuple[str, str]:
        return self.reasoning_by_example_turn[(example_id, turn)].strip(), completion.strip()


def harmony_model_specifics(reasoning_path: Path) -> ModelSpecifics:
    """A resumed run regenerates the example it was interrupted in, so a later sidecar line for the
    same (example_id, turn) replaces the earlier one."""
    reasoning_by_example_turn: ReasoningByExampleTurn = {}
    for line in reasoning_path.open():
        entry = json.loads(line)
        reasoning_by_example_turn[(entry["example_id"], entry["turn"])] = entry["reasoning"]
    return HarmonyModelSpecifics(reasoning_by_example_turn)
