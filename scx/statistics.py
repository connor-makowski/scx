"""
The statistics package is currently under construction
"""

import functools
from .utils import Error


class SummaryUtils(Error):
    @classmethod
    @functools.cache
    def __check_all_numbers__(self, vector: tuple):
        return all([isinstance(i, (float, int)) for i in vector])

    @classmethod
    @functools.cache
    def __sort_vector__(self, vector: tuple):
        return sorted(vector)

    @classmethod
    def validate(self, vector: tuple):
        if not self.__check_all_numbers__(vector):
            self.exception(
                "The provided vector contains items that are not numbers"
            )
        if len(vector) == 0:
            self.exception("The provided vector is empty")


class Summary(SummaryUtils):
    def __init__(self, vector: [list, tuple]):
        self.output = self.get_all(vector)

    @classmethod
    def get_all(self, vector: [list, tuple]):
        vector = tuple(vector)
        self.validate(vector)
        sorted_vector = self.__sort_vector__(tuple(vector))
        return {
            "mean": self.get_mean(vector),
            "mode": self.get_mode(vector),
            "min": float(min(vector)),
            "pct25": self.get_percentile(
                0.25, sorted_vector, validate_vector=False, is_sorted=True
            ),
            "median": self.get_percentile(
                0.50, sorted_vector, validate_vector=False, is_sorted=True
            ),
            "pct75": self.get_percentile(
                0.75, sorted_vector, validate_vector=False, is_sorted=True
            ),
            "max": float(max(vector)),
        }

    @classmethod
    def get_percentile(
        self,
        percentile: [float, int],
        vector: [list, tuple],
        validate_vector: bool = True,
        is_sorted: bool = False,
    ):
        if percentile > 1 or percentile < 0:
            self.exception("percentile must be between 0 and 1")
        if validate_vector:
            self.validate(tuple(vector))
        if not is_sorted:
            vector = self.__sort_vector__(tuple(vector))
        partial_idx = percentile * (len(vector) - 1)
        idx = int(partial_idx)
        lower_pct = 1 - (partial_idx - idx)
        upper_pct = partial_idx - idx
        return vector[idx] * lower_pct + vector[idx + 1] * upper_pct

    @classmethod
    def get_mode(self, vector: [list, tuple]):
        return float(max(set(vector), key=vector.count))

    @classmethod
    def get_mean(self, vector: [list, tuple]):
        return sum(vector) / len(vector)
