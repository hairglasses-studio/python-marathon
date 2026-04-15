def normalize(current: str, new_dir: str) -> str:
    # Decide starting stack based on absolute vs relative.
    if new_dir.startswith("/"):
        stack: list[str] = []
        path = new_dir
    else:
        # Seed from `current`. Empty segments and dots must be dropped too.
        stack = [seg for seg in current.split("/") if seg and seg != "."]
        path = new_dir

    for segment in path.split("/"):
        if not segment or segment == ".":
            continue
        if segment == "..":
            if stack:
                stack.pop()
            # else: already at root, stay there
        else:
            stack.append(segment)

    return "/" + "/".join(stack) if stack else "/"
