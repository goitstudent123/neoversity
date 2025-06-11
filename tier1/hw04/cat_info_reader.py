import json


def get_cats_info(path: str) -> list[dict[str, str]]:
    cats = []
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    continue  # skip malformed lines
                cat_id, name, age = parts
                cats.append({"id": cat_id, "name": name, "age": age})
        return cats

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Error while reading file: {e}")


if __name__ == "__main__":
    cats_info = get_cats_info("cats_file.txt")
    print(json.dumps(cats_info, indent=4))
