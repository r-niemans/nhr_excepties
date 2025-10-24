from nhr_template_creation.nhr_template_class import NHRDataFrame
import pandas as pd
from config.datasets_config import cohort_paths

pd.set_option('future.no_silent_downcasting', True)


def run_nhr_main(dataset_key):
    cohort_key = cohort_paths[dataset_key]

    nhr_df = NHRDataFrame(excel_path=cohort_key["original_file"],
                          sheet_name=cohort_key["sheet_name"],
                          header_row=cohort_key["header_row"])
    if dataset_key != "THI":
        nhr_df.apply_json_rules(cohort_key["json_rules"])
    nhr_df.export_file()

    print(f"NHR incl. Rules gemaakt voor {dataset_key}")
    return f"Bestand opgeslagen: {cohort_key['original_file']}"

