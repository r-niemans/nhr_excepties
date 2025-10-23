from nhr_template_creation.nhr_template_class import NHRDataFrame
import pandas as pd
from config.datasets_config import cohort_paths

pd.set_option('future.no_silent_downcasting', True)


def run_nhr_main(dataset_key):
    cohort_key = cohort_paths[dataset_key]

    nhr_df = NHRDataFrame(excel_input_path=cohort_key["input_file"], excel_output_path=cohort_key["output_file"], sheet_name=cohort_key["sheet_name"]) # output_file hier moet veranderd worden naar input_file aangezien het in dezelfde workbook terecht moet komen
    nhr_df.apply_json_rules(cohort_key["json_rules"])
    nhr_df.export_file(cohort_key["sheet_name"])

    print(f"✅ NHR-template voltooid voor {dataset_key}")
    return f"Bestand opgeslagen: {cohort_key['output_file']}"


def main():
    # alleen nodig als je het wilt testen voor een cohort
    dataset_key = "ABL"
    run_nhr_main(dataset_key)


if __name__ == "__main__":
    main()
