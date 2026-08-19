import json
import random
import os


DATA_FILE = "../data/pokec_sample.txt"
OUTPUT_FILE = "start_nodes.json"

NUMBER_OF_START_NODES = 100
RANDOM_SEED = 42


def get_source_nodes():

    source_nodes = set()

    with open(DATA_FILE, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            source = parts[0]

            source_nodes.add(source)

    return list(source_nodes)


def main():

    print("Reading dataset...")

    source_nodes = get_source_nodes()

    print(
        "Unique source nodes:",
        len(source_nodes)
    )

    random.seed(RANDOM_SEED)

    start_nodes = random.sample(
        source_nodes,
        NUMBER_OF_START_NODES
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            start_nodes,
            file,
            indent=4
        )

    print()
    print("Random start nodes created!")
    print(
        "Number of start nodes:",
        len(start_nodes)
    )
    print(
        "Random seed:",
        RANDOM_SEED
    )
    print(
        "Saved to:",
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()