# Typed Config Parser

**Tier:** tier1_fluency  
**Target time:** 12 minutes  
**Topics:** exception-hierarchy, string-parsing  
**Source:** `openai-python-refresher.ipynb` cells 75-78

## Problem

## 6.3 Exercise — Typed config parser

**Task:** Implement `parse_config(text)` that parses `key=value` pairs separated by newlines into a dict, raising appropriate custom exceptions on errors.

**Error cases:**
- Line has no `=`: raise `ConfigSyntaxError` with `line_number` attribute
- Key is empty: raise `ConfigSyntaxError`
- Duplicate key: raise `ConfigDuplicateKeyError` with `key` attribute
- Both should inherit from `ConfigError`

**Ignore:** empty lines and lines starting with `#` (comments).

## How to run

```bash
python marathon.py run 006
```

Edit `problem.py`. When `test_problem.py` passes, move on.
