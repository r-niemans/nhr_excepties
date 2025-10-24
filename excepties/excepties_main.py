import sys
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from config.datasets_config import cohort_paths
from excepties.excepties_functies import extract_exceptions_incremental


def run_exceptions(dataset_key: str):
    cfg = cohort_paths[dataset_key]
    file_path = cfg["original_file"]
    sheet = cfg["sheet_name"]
    header_row = cfg["header_row"]

    print(f"Lees NHR-template voor {dataset_key}: sheet='{sheet}', header={header_row}")

    nhr_data_df = pd.read_excel(file_path, sheet_name=sheet, header=header_row)

    print("Haal nieuwe excepties op")
    result_df = extract_exceptions_incremental(nhr_data_df, existing_wb_path=file_path)

    print(f"Excepties verwerkt en opgeslagen in '{file_path.name}' (sheet='Excepties')")

    return result_df


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python excepties_main.py <dataset>")
        sys.exit(1)

    dataset_key = sys.argv[1].upper()
    if dataset_key not in cohort_paths:
        print(f"Onbekende dataset: {dataset_key}")
        sys.exit(1)

    run_exceptions(dataset_key)
