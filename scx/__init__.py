import sys

if sys.version_info[0] == 3:
    pass
elif sys.version_info[0] < 3:
    raise Exception("Python version must be greater than or equal to 3")
