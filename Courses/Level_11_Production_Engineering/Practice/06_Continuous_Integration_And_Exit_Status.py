# Independent task: continuous integration & exit status
#
# Define run_tests(folder) to execute the current interpreter's -m pytest -q in the supplied
# project folder and return its actual exit code. Use subprocess without shell=True. In a
# TemporaryDirectory, create calc.py with double(value) and test_calc.py asserting normal and
# zero behavior, run the real tests, and print Pipeline exit: <code>. Exit the launcher with
# that same code so a failing test run cannot be masked. Pytest's own report and timing vary;
# the correct implementation ends with Pipeline exit: 0.

