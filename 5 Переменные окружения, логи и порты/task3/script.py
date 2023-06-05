import sys

print("Generating logs")

for i in range(1, 6):
    print(f"LOG - {i}")
    print(f"ERROR - {i}", file=sys.stderr)

print("Done")