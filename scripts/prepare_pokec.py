


from pathlib import Path
import csv
import gzip
import shutil


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

# Original Pokec relationship file.
# Put soc-pokec-relationships.txt.gz OR
# soc-pokec-relationships.txt inside data/ folder.
GZ_FILE = DATA_DIR / "soc-pokec-relationships.txt.gz"
RAW_FILE = DATA_DIR / "soc-pokec-relationships.txt"

NODES_FILE = DATA_DIR / "pokec_nodes.csv"
EDGES_FILE = DATA_DIR / "pokec_edges.csv"


def extract_dataset():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if RAW_FILE.exists():
        print(f"Dataset already extracted: {RAW_FILE}")
        return

    if not GZ_FILE.exists():
        print("\nPokec dataset file not found.")
        print("Please place one of these files inside the data folder:")
        print("  soc-pokec-relationships.txt.gz")
        print("OR")
        print("  soc-pokec-relationships.txt")
        print(f"\nExpected folder: {DATA_DIR}")
        raise FileNotFoundError("Pokec relationship dataset not found.")

    print("Extracting Pokec dataset...")

    with gzip.open(GZ_FILE, "rb") as src:
        with open(RAW_FILE, "wb") as dst:
            shutil.copyfileobj(src, dst)

    print("Extraction completed.")


def prepare_csv():
    print("Preparing Pokec CSV files...")

    nodes = set()
    edge_count = 0

    with open(
        RAW_FILE,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as source, open(
        EDGES_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as edge_output:

        edge_writer = csv.writer(edge_output)


        edge_writer.writerow(["src", "dst"])

        for line in source:
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            src = parts[0]
            dst = parts[1]

            nodes.add(src)
            nodes.add(dst)

            edge_writer.writerow([src, dst])

            edge_count += 1

            if edge_count % 1_000_000 == 0:
                print(f"Processed {edge_count:,} relationships...")

    print("Writing node CSV...")

    with open(
        NODES_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as node_output:

        node_writer = csv.writer(node_output)

        node_writer.writerow(["id"])

        for node_id in sorted(nodes, key=int):
            node_writer.writerow([node_id])

    print("\nPokec dataset prepared successfully!")
    print(f"Nodes: {len(nodes):,}")
    print(f"Edges: {edge_count:,}")
    print(f"Nodes file: {NODES_FILE}")
    print(f"Edges file: {EDGES_FILE}")

def main():
    print("=" * 50)
    print("Pokec Dataset Preparation")
    print("=" * 50)

    extract_dataset()
    prepare_csv()


if __name__ == "__main__":
    main()










