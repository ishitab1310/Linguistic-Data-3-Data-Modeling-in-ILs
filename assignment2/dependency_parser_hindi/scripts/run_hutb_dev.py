import os
import glob
import subprocess

INPUT_DIR = "data/hutb"
OUTPUT_DIR = "data/hutb_out"

os.makedirs(OUTPUT_DIR, exist_ok=True)

files = glob.glob(INPUT_DIR + "/*.dat")

for f in files:
    name = os.path.basename(f)
    out_file = os.path.join(OUTPUT_DIR, name + ".out")

    print("Parsing:", name)

    result = subprocess.run(
        ["python", "-m", "scripts.run_oracle", f],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    with open(out_file, "w", encoding="utf-8") as o:
        o.write(result.stdout)

print("DONE.")
