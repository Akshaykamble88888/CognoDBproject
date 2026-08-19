import statistics

def percentile(values, p):
    if not values:
        return None
    xs = sorted(values)
    k = (len(xs)-1) * p / 100
    f = int(k)
    c = min(f+1, len(xs)-1)
    if f == c:
        return xs[f]
    return xs[f] + (xs[c]-xs[f]) * (k-f)

def summarize(values):
    return {
        "count": len(values),
        "min_ms": min(values) if values else None,
        "p50_ms": percentile(values, 50),
        "p95_ms": percentile(values, 95),
        "avg_ms": statistics.mean(values) if values else None,
        "max_ms": max(values) if values else None,
    }
