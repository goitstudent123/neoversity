def total_salary(path: str) -> tuple[int, float]:
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            salaries = []
            for line in file:
                try:
                    _, salary = line.strip().split(",")
                    salaries.append(int(salary))
                except ValueError:
                    continue  # skip invalid lines

            if not salaries:
                return 0, 0.0

            total = sum(salaries)
            average = total // len(salaries)
            return total, average

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while processing file: {e}")


if __name__ == "__main__":
    total, average = total_salary("salaries.txt")
    print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
