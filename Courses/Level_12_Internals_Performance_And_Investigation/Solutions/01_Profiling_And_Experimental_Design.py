import cProfile
import pstats

profile = cProfile.Profile()
result = profile.runcall(sum, range(1000))
stats = pstats.Stats(profile)
print(f"Result: {result}")
print(f"Profiled calls: {stats.total_calls}")
