src = open("source.txt", "r")
dest = open("destination.txt", "w")

for line in src:
    if not line.startswith("#"):
        dest.write(line)

src.close()
dest.close()

print("Copied successfully!")
