"""
================================================================================
Level 3: Advanced Python
Lesson 1: Big-O Notation & Computational Complexity Analysis
================================================================================
📝 Quick Exercise Prompt:

Analyze the Big-O time complexity of this function:
```python
def find_pairs(nums, target):
    pairs = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                pairs.append((nums[i], nums[j]))
    return pairs
```
How can you optimize this to O(n) using a hash set?
================================================================================
"""

# Write your solution below:

