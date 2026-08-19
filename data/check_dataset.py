nodes = set()
relationships = 0

with open("soc-Pokec.txt", "r", encoding="utf-8") as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) < 2:
            continue

        source = parts[0]
        target = parts[1]

        nodes.add(source)
        nodes.add(target)

        relationships += 1


print("Nodes:", len(nodes))
print("Relationships:", relationships)