import random


INPUT_FILE = "soc-pokec.txt"
OUTPUT_FILE = "pokec_sample.txt"

TARGET_RELATIONSHIPS = 150_000
RANDOM_SEED = 42


def create_sample():

    random.seed(RANDOM_SEED)

    selected = []
    count = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip comments
            if line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            source = parts[0]
            target = parts[1]

            count += 1

            # Reservoir sampling
            if len(selected) < TARGET_RELATIONSHIPS:

                selected.append((source, target))

            else:

                index = random.randint(0, count - 1)

                if index < TARGET_RELATIONSHIPS:
                    selected[index] = (source, target)

    # Write sampled relationships to output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        for source, target in selected:

            file.write(f"{source} {target}\n")

    print("Sample created successfully!")
    print("Original relationships:", count)
    print("Sample relationships:", len(selected))
    print("Random seed:", RANDOM_SEED)
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":
    create_sample()