from scx.statistics import Summary

data=[4,3,3,2,2,1]
# Class based Usage
summary = Summary(data)
print(summary.output)

# Method based usage
print(Summary.get_all(data))
print(Summary.get_percentile(.50,data))
