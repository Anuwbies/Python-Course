# Independent task: free threading & runtime assumptions
#
# Report sys.implementation.name, the actual active GIL state when its probe exists (otherwise
# None), and the build's Py_GIL_DISABLED value. Run four joined threads performing 1000
# increments each under a shared Lock and print the actual count. The expected count is 4000;
# interpreter/build fields vary and must not be hardcoded. Record that a conventional-build run
# does not establish free-threaded compatibility.

