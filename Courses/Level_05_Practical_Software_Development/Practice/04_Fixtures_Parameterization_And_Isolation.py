# Independent task: fixtures, parameterization & isolation
#
# Define load_amounts(path) to load a JSON list of plain nonnegative integers or raise
# ValueError. Write a parameterized pytest test for [], [0], and [10, 20], writing each input
# through tmp_path and calling the real loader. Add one rejection test for [True].
#
# Expected behavior: the four collected cases pass independently and require no preexisting
# files.

