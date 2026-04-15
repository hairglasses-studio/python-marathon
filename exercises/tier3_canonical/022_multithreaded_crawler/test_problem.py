# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier3_canonical/022_multithreaded_crawler/

from problem import *  # noqa: F401,F403

def test_all():
    """Crawler tests — run after scaffold or reference solution."""
    import time
    import random


    def make_fetcher(graph: dict[str, list[str]]) -> Fetcher:
        """Return a fetcher that reads links from a static graph."""
        def _fetch(url: str) -> list[str]:
            if url not in graph:
                return []
            return list(graph[url])
        return _fetch


    def make_slow_fetcher(graph: dict[str, list[str]], delay: float = 0.05) -> Fetcher:
        def _fetch(url: str) -> list[str]:
            time.sleep(delay)
            return list(graph.get(url, []))
        return _fetch


    def make_flaky_fetcher(graph: dict[str, list[str]], fail_urls: set[str]) -> Fetcher:
        def _fetch(url: str) -> list[str]:
            if url in fail_urls:
                raise RuntimeError(f"boom on {url}")
            return list(graph.get(url, []))
        return _fetch


    # Simple graph:
    #   A -> [B, C]
    #   B -> [D]
    #   C -> [D, E]
    #   D -> []
    #   E -> [A]    (creates a cycle)
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D", "E"],
        "D": [],
        "E": ["A"],
    }

    # --- Gate 1: single-threaded BFS ---
    crawler = Crawler(make_fetcher(graph))
    result = crawler.crawl("A", max_pages=100)
    assert result == {"A", "B", "C", "D", "E"}, f"got: {result}"
    print("Gate 1a pass — basic BFS")

    # Respect max_pages
    small_result = crawler.crawl("A", max_pages=3)
    assert len(small_result) == 3
    assert "A" in small_result   # at least visited the seed
    print("Gate 1b pass — max_pages cap")

    # Flaky fetcher doesn't crash the crawl
    crawler = Crawler(make_flaky_fetcher(graph, fail_urls={"B"}))
    result = crawler.crawl("A", max_pages=100)
    assert "A" in result
    assert "B" not in result     # B failed to fetch
    assert "C" in result
    print("Gate 1c pass — flaky fetcher")

    # --- Gate 2: threaded version with shared visited set ---
    threaded = ThreadedCrawler(make_slow_fetcher(graph, delay=0.02), workers=4)
    result = threaded.crawl("A", max_pages=100)
    assert result == {"A", "B", "C", "D", "E"}, f"got: {result}"
    print("Gate 2a pass — threaded BFS")

    # Should actually be faster than sequential (though not always visibly so
    # on fast machines and small graphs)
    slow_fetcher = make_slow_fetcher(graph, delay=0.1)

    start = time.perf_counter()
    Crawler(slow_fetcher).crawl("A", max_pages=100)
    seq_time = time.perf_counter() - start

    start = time.perf_counter()
    ThreadedCrawler(slow_fetcher, workers=5).crawl("A", max_pages=100)
    par_time = time.perf_counter() - start

    print(f"  sequential: {seq_time:.2f}s")
    print(f"  threaded:   {par_time:.2f}s")
    assert par_time < seq_time + 0.05, "threaded should not be slower"
    print("Gate 2b pass — threaded is faster on I/O-bound")

    # --- Gate 3: max_pages with threaded ---
    big_graph = {f"url-{i}": [f"url-{j}" for j in range(i + 1, i + 5)] for i in range(50)}
    threaded = ThreadedCrawler(make_fetcher(big_graph), workers=4)
    result = threaded.crawl("url-0", max_pages=10)
    assert len(result) <= 10, f"got {len(result)} (should cap at 10)"
    assert len(result) >= 1
    print("Gate 3 pass — max_pages cap respected under parallelism")

    print("\nCrawler tests passed")
