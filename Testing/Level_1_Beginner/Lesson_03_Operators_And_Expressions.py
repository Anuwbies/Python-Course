"""
================================================================================
Level 1: Beginner Python
Lesson 3: Operators & Arithmetic Expressions
================================================================================
📝 Quick Exercise: Server Cluster Telemetry & Task Distribution

🏢 Real-Life Scenario:
You are building an automated telemetry diagnostic script for a cloud operations
center. The tool reads total server uptime in seconds, decomposes it into Days,
Hours, Minutes, and Seconds, and calculates task distribution across worker nodes.

📋 Requirements:
1. Capture inputs:
   - total_uptime_seconds (int)
   - total_jobs (int)
   - worker_nodes (int)
2. Decompose uptime using integer floor division (//) and modulus (%):
   - 1 Day = 86400s -> days, rem_days
   - 1 Hour = 3600s -> hours, rem_hours
   - 1 Minute = 60s -> minutes, seconds
3. Workload distribution:
   - jobs_per_worker = total_jobs // worker_nodes
   - unassigned_overflow = total_jobs % worker_nodes
4. Formulate boolean health checks:
   - meets_sla: days >= 1
   - is_perfectly_balanced: unassigned_overflow == 0
   - is_overloaded: (jobs_per_worker > 100) or (unassigned_overflow >= 5)
   - is_cluster_healthy: meets_sla and (not is_overloaded)
5. Output the structured telemetry report.

⚠️ Strict Constraint:
Use ONLY concepts covered in Lessons 1-3 (variables, primitives, input(), int(),
float(), arithmetic operators, comparison operators, logical operators,
f-strings, and print()). No if statements, no loops, no functions.
================================================================================
"""

# 1. Capture inputs
total_uptime_seconds = int(input("Enter server uptime in seconds: "))
total_jobs = int(input("Enter total pending batch jobs: "))
worker_nodes = int(input("Enter active worker server count: "))

# 2. Decompose uptime
days = total_uptime_seconds // 86400
rem_days = total_uptime_seconds % 86400

hours = rem_days // 3600
rem_hours = rem_days % 3600

minutes = rem_hours // 60
seconds = rem_hours % 60

# 3. Workload distribution
jobs_per_worker = total_jobs // worker_nodes
unassigned_overflow = total_jobs % worker_nodes

# 4. Diagnostic boolean evaluations
meets_sla = days >= 1
is_perfectly_balanced = unassigned_overflow == 0
is_overloaded = (jobs_per_worker > 100) or (unassigned_overflow >= 5)
is_cluster_healthy = meets_sla and (not is_overloaded)

# 5. Formatted telemetry output
print("\n==================================================")
print("        CLOUD CLUSTER TELEMETRY REPORT            ")
print("==================================================")
print(f"Uptime Breakdown: {days}d {hours}h {minutes}m {seconds}s (Total: {total_uptime_seconds}s)")
print("--------------------------------------------------")
print("WORKLOAD DISTRIBUTION:")
print(f"Total Batch Jobs:    {total_jobs}")
print(f"Active Worker Nodes: {worker_nodes}")
print(f"Jobs Per Node:       {jobs_per_worker}")
print(f"Unassigned Backlog:  {unassigned_overflow}")
print("--------------------------------------------------")
print("DIAGNOSTIC HEALTH CHECKS:")
print(f"Meets 24h SLA:       {meets_sla}")
print(f"Perfect Load Split:  {is_perfectly_balanced}")
print(f"Cluster Overloaded:  {is_overloaded}")
print(f"Cluster Healthy:     {is_cluster_healthy}")
print("==================================================")
