# Hints for FizzBuzz

## Hint 1

This is a conditional classification problem over a range of integers. Think about how Python's `%` (modulo) operator tells you divisibility, and consider the order in which you check conditions — one case is a combination of two others, so it must be checked first.

## Hint 2

Approach outline:
- Build a result list by iterating `range(1, n + 1)`
- For each number, check divisibility in the right order: both-3-and-5 first, then 3 alone, then 5 alone
- Use `str(i)` as the fallback when no condition matches
- Append each label to the list and return it

## Hint 3

```python
result = []
for i in range(1, n + 1):
    if i % 15 == 0:
        result.append("FizzBuzz")
    elif i % 3 == 0:
        ...
```
