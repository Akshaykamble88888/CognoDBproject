import time
import statistics


def percentile(values, percent):

    values = sorted(values)

    index = int(
        (percent / 100) * (len(values) - 1)
    )

    return values[index]


def run_query(
    session,
    query,
    parameters=None,
    iterations=100,
    warmup=10
):

    if parameters is None:
        parameters = {}

    # Warm-up
    for _ in range(warmup):

        session.run(
            query,
            parameters
        ).consume()

    timings = []

    # Actual benchmark
    for _ in range(iterations):

        start = time.perf_counter()

        session.run(
            query,
            parameters
        ).consume()

        end = time.perf_counter()

        latency_ms = (
            end - start
        ) * 1000

        timings.append(latency_ms)

    return {
        "p50_ms": percentile(
            timings,
            50
        ),
        "p95_ms": percentile(
            timings,
            95
        ),
        "min_ms": min(timings),
        "max_ms": max(timings),
        "avg_ms": statistics.mean(timings),
        "iterations": iterations
    }