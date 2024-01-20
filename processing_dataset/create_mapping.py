import argparse
import os
from tqdm import tqdm
import json

def create_mapping(data_root_path, mapping_path="mapping.json"):
    if os.path.exists(mapping_path):
        raise Exception("mapping.json is already exist")
    else:
        categories = os.listdir(data_root_path)
        mapping = {}

        with open(mapping_path, 'w', encoding="utf-8") as f:
            for i, category in enumerate(tqdm(categories)):
                mapping[i] = category
            json.dump(mapping, f)

    print("Finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_root_path", type=str, required=True)
    parser.add_argument("--mapping_path", type=str, default="mapping.json")
    args = parser.parse_args()
    create_mapping(args.data_root_path, args.mapping_path)