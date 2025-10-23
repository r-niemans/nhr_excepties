import sys
import pandas as pd
from pathlib import Path
from config.datasets_config import cohort_paths
from excepties.excp_pt3 import extract_exceptions_incremental


def run_exceptions(dataset_key: str):
    cfg = cohort_paths[dataset_key]
    file_path = cfg["input_file"]
    sheet = cfg["sheet_name"]
    header_row = cfg["header_row"]

    print(f"📖 Lees NHR-template voor {dataset_key}: sheet='{sheet}', header={header_row}")

    # --- 1️⃣ Inlezen van de benodigde sheets
    all_data_df = {
        "NHR_Template": pd.read_excel(file_path, sheet_name=sheet, header=header_row),
        "Excepties": pd.read_excel(file_path, sheet_name="Excepties")
    }

    nhr_data = all_data_df["NHR_Template"]

    # --- 2️⃣ Bepaal de excepties
    print("Extract exceptions incrementally...")
    result_df = extract_exceptions_incremental(nhr_data, existing_wb_path=file_path)

    # --- 3️⃣ Schrijf resultaat terug naar hetzelfde Excelbestand
    print("Schrijf excepties terug naar Excel...")
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        result_df.to_excel(writer, sheet_name="Excepties", index=False)

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