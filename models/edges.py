from dataclasses import dataclass
from typing import Tuple


@dataclass
class Edge:
    __slots__ = ["start", "end"]
    start: int
    end: int

    def to_tuple(self) -> Tuple[str, str]:
        return str(self.start), str(self.end)

    def __hash__(self):
        if self.start > self.end:
            return hash(f"{self.start} {self.end}")
        else:
            return hash(f"{self.end} {self.start}")

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.end == other.end
            or self.end == other.start
            and self.start == other.end
        )


@dataclass
class WeightedEdge(Edge):
    weight: int
    __slots__ = ["start", "end", "weight"]

    def to_tuple(self) -> Tuple[str, str, float]:
        return str(self.start), str(self.end), float(self.weight)

    def __hash__(self):
        if self.start > self.end:
            return hash(f"{self.start} {self.end}")
        else:
            return hash(f"{self.end} {self.start}")

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.end == other.end
            or self.end == other.start
            and self.start == other.end
        )
