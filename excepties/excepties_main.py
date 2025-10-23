import pandas as pd
import re
from excepties.excp_pt3 import *
import sys
from pathlib import Path
import shutil

"""
run in terminal middels het volgende:
python excepties\\excepties_main.py 'L:\\CVPZ\\CHVC\\MANAGEMENT\\BIM\\Python_Programmas\\ablaties\\ABL_Epic_Verrichtingen_CAR.xlsx' 'L:\\CVPZ\\CHVC\\MANAGEMENT\\BIM\\Python_Programmas\\ablaties\\exceptions_df.xlsx'
"""

source = r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_ABL_Epic_Verrichtingen_CAR.xlsx"
target = r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\ablaties\ABL_Epic_Verrichtingen_CAR.xlsx"

shutil.copy(source, target) #kopieer de meest recente versie van de originele verrichtingen file naar de folder

directory = Path(r'L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic')
#path_matches = list(directory.glob("*Epic_Verrichtingen_CAR*.xlsx"))
#user_input = input("Voor welk cohort moeten excepties worden opgehaald?") -> ABL, PCI, PMICD, OHO, THI
#input_path = [file for file in path_matches if "{user_input}" in path_matches]

if __name__ == "__main__":
    if len(sys.argv) < 2: #moet eig < 3 zijn
        print("Gebruik in terminal als volgt: python excepties_main.py <excel_input_path> <excel_output_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    all_data_df = {"ABL_NHR_Template": pd.read_excel(file_path, sheet_name="ABL NHR template", header=6), #ervanuitgaande dat het bestand beide sheets bevat
                   "Excepties": pd.read_excel(file_path, sheet_name="Excepties")
                   }
    nhr_data = all_data_df['ABL_NHR_Template'] #want hier worden de rules toegepast dus NADAT de rules zijn toegepast
    excepties = all_data_df['Excepties']
    result_df = extract_exceptions_incremental(nhr_data, existing_wb_path= file_path)

