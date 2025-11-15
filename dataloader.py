from datasets import load_dataset
from pathlib import Path

OUT_DIR = Path("data/TravelPlanner")
OUT_DIR.mkdir(parents=True, exist_ok=True)

for config in ["train", "validation", "test"]:
    ds_dict = load_dataset("osunlp/TravelPlanner", config)
    for split_name, ds in ds_dict.items():
        ds.to_csv(str(OUT_DIR / f"{config}_{split_name}.csv"))
        ds.to_json(str(OUT_DIR / f"{config}_{split_name}.jsonl"), orient="records", lines=True)

print(str(OUT_DIR.resolve()))