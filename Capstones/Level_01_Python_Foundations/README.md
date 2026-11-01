# Level 1 capstone: weekly budget calculator

**Prerequisites:** All eight [Python Foundations lessons](../../Courses/Level_01_Python_Foundations/README.md). **Submission:** [Practice/weekly_budget.py](Practice/weekly_budget.py).

Build a small interactive calculator for a student's planned weekly spending. The project brings together named values, text input, conversion, arithmetic, string cleanup, and formatted output. It uses a straight sequence of statements so you can explain the complete data flow before learning conditions, loops, or custom functions.

## 1. Define what the calculator accepts

Read these six responses in this order:

| Input | Accepted value | Meaning |
| --- | --- | --- |
| Name | Nonempty text after surrounding whitespace is removed | Person receiving the report |
| Weekly budget | Nonnegative integer | Whole pesos available for the week |
| Study days | Positive integer | Days on which the daily costs occur |
| Daily transport | Nonnegative integer | Whole-peso transport cost on each study day |
| Daily food | Nonnegative integer | Whole-peso food cost on each study day |
| Other weekly costs | Nonnegative integer | One weekly amount, counted once |

The task assumes valid responses. Validation, repeated prompting, and exception recovery are later-level features. State these assumptions in a short source comment rather than copying advanced syntax into this program.

Use these prompt lines, each printed before its corresponding `input()` call:

```text
Name:
Weekly budget (whole PHP):
Study days:
Daily transport (whole PHP):
Daily food (whole PHP):
Other weekly costs (whole PHP):
```

The name stays text and is cleaned with `.strip()`. Convert the five numeric responses to integers. Preserve a meaningful internal space or accent in a name.

## 2. Work out the relationships before coding

| Result | Formula | Reason |
| --- | --- | --- |
| Weekly transport | Daily transport × study days | Transport occurs on each study day |
| Weekly food | Daily food × study days | Food occurs on each study day |
| Planned spending | Weekly transport + weekly food + other weekly costs | Other costs already cover the week |
| Remaining | Weekly budget − planned spending | A negative value represents an overspending plan |
| Average planned per day | Planned spending ÷ study days | A displayed average across those days |
| Whole-peso daily budget | Weekly budget floor-divided by study days | Equal whole-unit allocation of available budget |
| Unallocated from daily split | Weekly budget remainder study days | Budget units not included in that equal allocation |

The average planned cost and whole-peso daily budget answer different questions. One summarizes spending; the other divides available money. Do not substitute one for the other.

Keep a negative remaining value. For example, spending 280 from a budget of 200 leaves -80. Returning 0 instead would hide the size of the shortfall. Level 2 can later add a status message using a condition; Level 1 only displays the correct numeric balance.

The remainder belongs to the equal split of the **budget**, not the division of planned spending. Whole shares multiplied by days plus the unallocated remainder should reconstruct the original budget.

## 3. Produce a report from the calculated values

After the prompts and input, print a blank line, the title `WEEKLY BUDGET`, and the following fields in order. Use integer displays for whole-peso totals and two decimal places only for the average.

Sample response lines:

```text
Mika
1000
5
40
100
150
```

Expected report after the input prompts:

```text

WEEKLY BUDGET
Name: Mika
Budget: PHP 1000
Days: 5
Transport: PHP 200
Food: PHP 500
Other: PHP 150
Planned spending: PHP 850
Remaining: PHP 150
Average planned per day: PHP 170.00
Whole-peso daily budget: PHP 200
Unallocated from daily split: PHP 0
```

For this case, transport costs `40 * 5 = 200`, food costs `100 * 5 = 500`, and the weekly other cost is 150. Planned spending is therefore 850, leaving 150 of the 1000 budget. The report should reflect the variables you calculated; do not print fixed answers that only match the sample.

## 4. Build in small stages

First, write the input section and make sure you understand each value's type. Second, calculate the weekly totals using named intermediate results. Third, add the report. Run the normal example, then change the input values one group at a time.

Save and run your own file from the repository root:

```powershell
python Capstones/Level_01_Python_Foundations/Practice/weekly_budget.py
```

An empty starter prints nothing until you implement it. Use the hints below if you are stuck; the full [reference solution](Solutions/weekly_budget.py) is separate.

<details>
<summary>Hint 1: reading values</summary>

Use `print()` for each prompt, then `input()` for the response. The numeric responses need `int()`. The name needs text cleanup, not numeric conversion.

</details>

<details>
<summary>Hint 2: avoid counting a weekly cost multiple times</summary>

Compute transport and food as separate daily-cost-times-days totals. Add the other weekly amount once after those multiplications.

</details>

<details>
<summary>Hint 3: distinguish the two divisions</summary>

Use `/` for the average planned spending. Use `//` and `%` on the available budget for the equal whole-peso split and its remainder.

</details>

## 5. Try these manual scenarios

| Scenario | Responses after the name: budget, days, transport, food, other | Important expected results |
| --- | --- | --- |
| Normal plan | `1000, 5, 40, 100, 150` | Spending 850; remaining 150; average 170.00 |
| Zero costs | `0, 3, 0, 0, 0` | All monetary results 0; average 0.00 |
| Uneven allocation | `1001, 4, 10, 20, 50` | Spending 170; remaining 831; average 42.50; daily budget 250; remainder 1 |
| Overspending | `200, 3, 50, 40, 10` | Spending 280; remaining -80; average 93.33; daily budget 66; remainder 2 |
| A single day | `500, 1, 30, 70, 50` | Spending 150; remaining 350; daily budget 500; remainder 0 |

Also use a name such as `  José Santos  ` and explain why the report should display `José Santos`. Enter each numeric response on its own line; the comma-separated groups in the table describe the scenarios and are not literal input lines.

## 6. Ask for a code review

When ready, ask the assistant to review your saved capstone. A complete review should establish that:

- The program uses only Level 1 concepts, and each numeric response is converted appropriately.
- The formulas match the stated units and count the weekly other cost once.
- The report follows the actual inputs and includes a correct remainder and negative balance when applicable.
- Formatting is applied to display, while the calculation values remain numeric.
- You can explain the difference between spending, remaining money, average cost, and whole-unit allocation.
- You can make a small change, such as adding a weekly book expense, while explaining the updated formula.

Record the result, saved file path, and topics to revisit in [Level 1 progress](../../Progress/Level_01_Python_Foundations.md). Reading or running the reference is not completion of your submission.

**Later retrieval:** At a later session, reconstruct the planned-spending formula and the quotient/remainder relationship without opening the solution.

Continue with [Level 2: Control Flow & Collections](../../Courses/Level_02_Control_Flow_And_Collections/README.md) to manage multiple entries and react to a budget balance.
