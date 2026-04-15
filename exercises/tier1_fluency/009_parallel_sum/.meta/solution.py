from concurrent.futures import ThreadPoolExecutor


def parallel_sum(numbers: list[int], chunk_size: int, max_workers: int = 4) -> int:
    if not numbers:
        return 0
    chunks = [
        numbers[i:i + chunk_size]
        for i in range(0, len(numbers), chunk_size)
    ]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        chunk_sums = pool.map(sum, chunks)
        return sum(chunk_sums)
