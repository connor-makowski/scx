"""
NOTE: The statistics package is currently under construction
"""

import functools, type_enforced
from .utils import Error


@type_enforced.Enforcer
class Summary(Error):
    @staticmethod
    def __get_vector__(vector:[tuple[int,float],list[int,float]]) -> tuple[int,float]:
        if len(vector) == 0:
            self.exception("The provided vector is empty")
        return tuple(sorted(vector))

    @staticmethod
    def get_all_summary_stats(vector: [list, tuple]) -> dict[float]:
        vector = Summary.__get_vector__(vector)
        return {
            "mean": Summary.get_mean(vector),
            "mode": Summary.get_mode(vector),
            "min": float(min(vector)),
            "pct25": Summary.get_percentile(
                0.25, vector, vector_is_checked=True
            ),
            "median": Summary.get_percentile(
                0.50, vector, vector_is_checked=True
            ),
            "pct75": Summary.get_percentile(
                0.75, vector, vector_is_checked=True
            ),
            "max": float(max(vector)),
        }

    @staticmethod
    def get_percentile(
        percentile: [float,int],
        vector: [list,tuple],
        vector_is_checked: bool = False,
    ) -> float:
        if not vector_is_checked:
            vector = Summary.__get_vector__(vector)
        if percentile > 1 or percentile < 0:
            self.exception("`percentile` must be between 0 and 1")
        partial_idx = percentile * (len(vector) - 1)
        idx = int(partial_idx)
        lower_pct = 1 - (partial_idx - idx)
        upper_pct = partial_idx - idx
        return float(vector[idx] * lower_pct + vector[idx + 1] * upper_pct)

    @staticmethod
    def get_mode(vector: [list,tuple], vector_is_checked: bool = False) -> float:
        if not vector_is_checked:
            vector = Summary.__get_vector__(vector)
        return float(max(set(vector), key=vector.count))

    @staticmethod
    def get_mean(vector: [list,tuple], vector_is_checked: bool = False) -> float:
        if not vector_is_checked:
            vector = Summary.__get_vector__(vector)
        return float(sum(vector) / len(vector))

