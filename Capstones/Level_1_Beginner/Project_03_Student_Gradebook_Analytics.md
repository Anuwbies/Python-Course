# Capstone Project 1.3: Student Gradebook & Analytics Engine

## 📌 Project Overview
Develop a **Student Gradebook & Academic Analytics CLI** that processes student assessment data, computes descriptive statistics (Mean, Median, Standard Deviation, Letter Grades), applies custom grading curves, ranks students, and exports comprehensive analytical reports to disk.

---

## 🎯 Learning Objectives
- **Data Structures**: Deeply manipulate nested dictionaries and lists (`Dict[str, Dict[str, List[float]]]`).
- **Mathematical Algorithms**: Implement core statistical calculations using pure Python (without NumPy).
- **String Formatting**: Generate aligned, professional ASCII reports and summary dashboards.
- **CSV & Text File Processing**: Parse raw student CSV input files and generate CSV report outputs.
- **Defensive Design**: Validate grades within bounds ($0.0 \le \text{grade} \le 100.0$) and handle missing entries.

---

## 🏗️ System Architecture

```text
+-------------------------------------------------------------+
|                     Gradebook Manager                       |
+-------------------------------------------------------------+
                               |
            +------------------+------------------+
            |                                     |
+----------------------+              +----------------------+
|    Student Record    |              |   Analytics Engine   |
+----------------------+              +----------------------+
| - id: str            |              | + calculate_mean()   |
| - name: str          |              | + calculate_median() |
| - scores: dict       |              | + calculate_std_dev()|
| + get_average()      |              | + apply_curve()      |
| + get_letter_grade() |              | + generate_report()  |
+----------------------+              +----------------------+
```

---

## 📋 Functional Requirements

### 1. Student Record Model
Each student possesses:
- `student_id`: Unique identifier (e.g., `"STU-8801"`).
- `name`: Full name string.
- `scores`: A dictionary of category scores (e.g., `{"quizzes": [85, 90, 78], "midterm": 88, "final": 92}`).

### 2. Weighted Grading Calculation
Grades are calculated according to customizable category weights:
- Quizzes: 20%
- Assignments: 30%
- Midterm Exam: 20%
- Final Exam: 30%
- **Final Weighted Score Formula**:
  $$\text{Final Grade} = \sum (\text{Category Average} \times \text{Weight})$$

### 3. Grading Scale & Letter Mapping
- $\ge 90.0$: `A`
- $\ge 80.0$: `B`
- $\ge 70.0$: `C`
- $\ge 60.0$: `D`
- $< 60.0$: `F`

### 4. Statistical Engine (Pure Python)
Compute across the entire classroom:
- **Class Mean**: $\mu = \frac{1}{N} \sum x_i$
- **Class Median**: Middle value of sorted scores.
- **Standard Deviation**: $\sigma = \sqrt{\frac{1}{N} \sum (x_i - \mu)^2}$
- **Highest & Lowest Scorers**.

### 5. Report Exporter
- Print an interactive summary table to terminal.
- Export a detailed breakdown report to `grade_report.txt` and `grade_summary.csv`.

---

## 📐 Phased Implementation Guide

### Phase 1: Pure Statistical Helpers
```python
import math

def calculate_mean(numbers: list[float]) -> float:
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

def calculate_median(numbers: list[float]) -> float:
    if not numbers:
        return 0.0
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 1:
        return sorted_nums[mid]
    return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0

def calculate_std_dev(numbers: list[float]) -> float:
    if len(numbers) < 2:
        return 0.0
    mean = calculate_mean(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    return math.sqrt(variance)
```

### Phase 2: Student Class
```python
class Student:
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.quizzes = []
        self.assignments = []
        self.midterm = 0.0
        self.final_exam = 0.0

    def calculate_final_grade(self, weights: dict) -> float:
        quiz_avg = calculate_mean(self.quizzes) if self.quizzes else 0.0
        assign_avg = calculate_mean(self.assignments) if self.assignments else 0.0
        
        total = (
            quiz_avg * weights.get("quizzes", 0.2) +
            assign_avg * weights.get("assignments", 0.3) +
            self.midterm * weights.get("midterm", 0.2) +
            self.final_exam * weights.get("final", 0.3)
        )
        return round(total, 2)
```

### Phase 3: CSV Importer / Exporter & Gradebook Engine
Parse CSV files in the format `student_id,name,quiz1,quiz2,assign1,midterm,final` and export summary statistics.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Empty Score List** | Student with no assignments submitted | Safely defaults assignment average to 0.0 without division by zero |
| **Invalid Grade Range** | Enter grade `105` or `-10` | Raises `ValueError` informing user grade must be between 0 and 100 |
| **Tied Median** | Class with even number of students (e.g. 4 students) | Computes average of the two middle scores correctly |
| **Curve Adjustment** | Apply +5 point curve across class | Recomputes letter grades, capping max possible score at 100.0 |

---

## 🚀 Bonus Challenges
- **Bell Curve Normalization**: Implement automatic Gaussian bell-curve grading ($Z$-scores).
- **Interactive Visual Histogram**: Render a horizontal ASCII bar chart of grade distribution in terminal (e.g., `A: ██████ (6)`, `B: ████████ (8)`).
