import sys
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from config.datasets_config import cohort_paths
from excepties.excepties_functies import extract_exceptions_incremental

def run_exceptions(dataset_key: str, var_type: str = "Interventievariabelen"):
    cfg = cohort_paths[dataset_key]
    file_path = cfg["original_file"]
    sheet = cfg["sheet_name"]
    header_row = cfg["header_row"]
    kolomlijst_file = cfg["input_variables_path"]

    print(f"Lees '{sheet}', header={header_row}")
    nhr_data_df = pd.read_excel(file_path, sheet_name=sheet, header=header_row)

    if kolomlijst_file and Path(kolomlijst_file).exists():
        print(f"Gebruik kolomlijst: {kolomlijst_file}")
        kolommen = pd.read_excel(kolomlijst_file)

        # Regex to classify columns
        pattern = r"interv" if "Interventie" in var_type else r"followup"
        kolommen = kolommen[kolommen["Bron"].astype(str).str.contains(pattern, case=False, na=False)]

        relevant_cols = kolommen["Kolomnaam"].tolist()
        relevant_cols = [c for c in relevant_cols if c in nhr_data_df.columns]

        print(f"Geselecteerde kolommen voor {var_type}: {len(relevant_cols)} gevonden.")
        nhr_data_df = nhr_data_df[["pat_nr", "interv_nr", "interv_datum"] + relevant_cols]
        # Remove duplicate column names — keeps first occurrence only
        nhr_data_df = nhr_data_df.loc[:, ~nhr_data_df.columns.duplicated()].copy()

        # Flatten MultiIndex (if it exists)
        if isinstance(nhr_data_df.columns, pd.MultiIndex):
            nhr_data_df.columns = ['_'.join(map(str, col)).strip() for col in nhr_data_df.columns]

    else:
        print("Geen kolomlijst gevonden, gebruik alle kolommen.")

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
