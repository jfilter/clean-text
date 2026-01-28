# Benchmarks

## `clean_texts()` — sequential vs. parallel

Run the benchmark:

```bash
python benchmarks/bench_clean_texts.py
```

### Setup

- 10 unique sample texts repeated to reach the target corpus size
- All cleaning options enabled (`no_urls`, `no_emails`, `no_phone_numbers`, `no_ip_addresses`, `no_file_paths`, `no_code`, `no_currency_symbols`, `lang="de"`)
- Machine: 10 CPU cores, Python 3.12

### Results

| Texts   | n_jobs=1       | n_jobs=2       | n_jobs=5       | n_jobs=10      | n_jobs=-1      |
|--------:|----------------|----------------|----------------|----------------|----------------|
|     100 | 0.021s (1.00x) | 0.641s (0.03x) | 0.616s (0.03x) | 0.887s (0.02x) | 0.869s (0.02x) |
|   1,000 | 0.208s (1.00x) | 0.704s (0.30x) | 0.657s (0.32x) | 0.980s (0.21x) | 0.932s (0.22x) |
|  10,000 | 2.091s (1.00x) | 1.695s (1.23x) | 1.083s (1.93x) | 1.346s (1.55x) | 1.284s (1.63x) |

### Takeaways

- **Small batches (< 1,000):** Sequential (`n_jobs=1`) is fastest. Process spawning and IPC overhead far exceed the per-text work.
- **Large batches (10,000+):** Parallel processing pays off. Best speedup observed was ~1.9x with `n_jobs=5` on a 10-core machine.
- **More workers != faster:** Beyond a sweet spot, adding workers increases coordination overhead without proportional gains. The optimal `n_jobs` depends on corpus size and hardware.
- **Default is safe:** `n_jobs=1` (the default) adds zero overhead, so existing single-text and small-batch workflows are unaffected.
