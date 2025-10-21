from nhr_template_class import NHRDataFrame
import pandas as pd

pd.set_option('future.no_silent_downcasting', True)
def main():
    input_path = r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_ABL_Epic_Verrichtingen_CAR.xlsx"
    output_path = r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\ablaties\ablaties_NHR_template.xlsx"

    nhr_df = NHRDataFrame(input_path, output_path)
    nhr_df.apply_json_rules(r"abl_rules.json")
    nhr_df.export_file()


if __name__ == '__main__':
    main()