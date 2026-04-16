# Notes for Stack-Based Path Normalization

## Why this matters

Path normalization is a ubiquitous systems problem: shells, file servers, web routers, and security sandboxes all need to canonicalize paths. Path traversal attacks (`../../etc/passwd`) exploit systems that don't normalize correctly before checking access.

## Watch out for

- **Absolute vs relative**: if `new_dir` starts with `/`, `current` is irrelevant. Concatenating them blindly is a common mistake.
- **Root boundary**: `..` from `/` should stay at `/`, not go to an empty or negative stack. Guard with `if stack` before popping.
- **Empty components from double slashes**: `a//b` splits into `["a", "", "b"]`. Skip empty strings.

## Interview follow-ups

1. How would you extend this to handle `~` (home directory expansion)?
2. What security implications arise if path normalization happens after access control checks rather than before?
3. How does this compare to `os.path.normpath`? What cases does the stdlib function not handle (e.g., the relative-to-current-dir aspect)?
