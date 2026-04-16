# Hints for Stack-Based Path Normalization

## Hint 1

This is a stack problem disguised as string processing. Process the path components one at a time: `..` means pop from the stack (but never below empty), `.` means do nothing, empty strings (from double slashes) mean do nothing, and everything else is pushed. If `new_dir` starts with `/`, it's absolute — ignore `current` entirely.

## Hint 2

Step-by-step:
- Check if `new_dir` starts with `/`. If so, set the working path to `new_dir`; otherwise prepend `current + "/" + new_dir` to get the full path to resolve
- Split the full path on `"/"` to get components
- Walk each component: skip empty strings and `"."`, pop the stack for `".."` (only if stack is non-empty), otherwise push the component
- Return `"/" + "/".join(stack)` (which equals `"/"` when the stack is empty)

## Hint 3

The stack-processing loop:

```python
stack = []
for part in full_path.split("/"):
    if part == "" or part == ".":
        continue
    elif part == "..":
        if stack:
            stack.pop()
    else:
        stack.append(part)
return "/" + "/".join(stack)
```
