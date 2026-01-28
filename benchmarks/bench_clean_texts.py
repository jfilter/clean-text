"""Benchmark sequential vs. parallel clean_texts().

Run:
    python benchmarks/bench_clean_texts.py

Generates a batch of texts and compares wall-clock time for different n_jobs
values. Results will vary by machine — this is meant for manual inspection,
not CI assertions.
"""

import logging
import os
import time

# Suppress noisy warnings from worker processes (e.g. unidecode fallback)
logging.disable(logging.WARNING)

from cleantext import clean, clean_texts

# ── sample data ──────────────────────────────────────────────────────────────

SAMPLE_TEXTS = [
    "Hello, world!  This is    some text with   irregular spacing.",
    "Visit https://example.com/path?q=1&r=2 for more info.",
    "Contact us at support@example.com or call +1-555-123-4567.",
    "Price is $1,299.99 or €1,199.99 — what a deal!",
    "Äpfel, Birnen und Grüße aus München 🎉🍎",
    "Check the code:\n```python\nprint('hello')\n```\nThat's it.",
    "Edit /etc/nginx/nginx.conf and C:\\Users\\Admin\\file.txt carefully.",
    "Server IP: 192.168.1.1 and 2001:db8::1 are both valid.",
    'A bunch of \\u2018new\\u2019 references with "broken" unicode.',
    "»Yóù àré     rïght &lt;3!«  🤔 🙈 emoji test 👩🏾\u200d🎓",
]

KWARGS = dict(
    no_urls=True,
    no_emails=True,
    no_phone_numbers=True,
    no_ip_addresses=True,
    no_file_paths=True,
    no_code=True,
    no_currency_symbols=True,
    lang="de",
)


def build_corpus(n):
    """Repeat SAMPLE_TEXTS to reach *n* total texts."""
    repeats, remainder = divmod(n, len(SAMPLE_TEXTS))
    return SAMPLE_TEXTS * repeats + SAMPLE_TEXTS[:remainder]


def bench(corpus, n_jobs, warmup=False):
    """Time a single clean_texts() call and return elapsed seconds."""
    start = time.perf_counter()
    result = clean_texts(corpus, n_jobs=n_jobs, **KWARGS)
    elapsed = time.perf_counter() - start
    return elapsed, result


def main():
    cpu_count = os.cpu_count() or 1
    sizes = [100, 1_000, 10_000]
    jobs_list = [1, 2, max(1, cpu_count // 2), cpu_count, -1]
    # deduplicate while preserving order
    jobs_list = list(dict.fromkeys(jobs_list))

    print(f"CPUs detected: {cpu_count}")
    print(f"Sample texts:  {len(SAMPLE_TEXTS)} unique, cleaning kwargs: {list(KWARGS.keys())}")
    print()

    for size in sizes:
        corpus = build_corpus(size)
        print(f"── {size:,} texts {'─' * 50}")

        # warmup (first multiprocessing call spawns workers)
        bench(corpus[:10], n_jobs=1)

        baseline = None
        for n_jobs in jobs_list:
            elapsed, result = bench(corpus, n_jobs)
            if baseline is None:
                baseline = elapsed
            speedup = baseline / elapsed if elapsed > 0 else float("inf")
            label = f"n_jobs={n_jobs:<4}"
            if n_jobs == -1:
                label = f"n_jobs=-1 ({cpu_count} CPUs)"
            print(f"  {label:28s}  {elapsed:8.3f}s   {speedup:5.2f}x")

        # sanity: sequential and parallel produce identical output
        seq = clean_texts(corpus, n_jobs=1, **KWARGS)
        par = clean_texts(corpus, n_jobs=-1, **KWARGS)
        assert seq == par, "MISMATCH between sequential and parallel results!"
        print(f"  ✓ sequential == parallel output verified")
        print()


if __name__ == "__main__":
    main()
