# Notes for FizzBuzz

## Why this matters

FizzBuzz is used as a warm-up gate in interviews to confirm that a candidate can translate a multi-branch rule into working code immediately, without hesitation. The real test is condition ordering — many candidates check 3 and 5 individually before handling the combined case, producing wrong output for multiples of 15.

## Watch out for

- Checking `% 3` or `% 5` before the `% 15` (combined) case causes multiples of 15 to be misclassified as "Fizz"
- Off-by-one: the range must be `1..n` inclusive, so use `range(1, n + 1)`, not `range(n)`

## Interview follow-ups

- "Can you write this as a one-liner using a list comprehension?"
- "How would you extend this to also print 'Jazz' for multiples of 7?"
- "What would change if the output needed to be a generator instead of a list?"
