from scx.statistics import Summary

# Simple Test Data
data=[4,3,3,3,2,2,1,4,5,3]
# Summary Usage
if Summary.get_all_summary_stats(data) != {
    "mean": 3.0,
    "mode": 3.0,
    "min": 1.0,
    "pct25": 2.25,
    "median": 3.0,
    "pct75": 3.75,
    "max": 5.0
}:
    raise Exception("Summary staticmethod test failed")
