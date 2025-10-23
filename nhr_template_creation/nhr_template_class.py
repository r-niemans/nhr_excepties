# gebruik ofwel mijn oude script of maak een class aan waar alle rules instaan
# die dan aangeroepen kunnen worden
# !!! zorg dat mijn script zowel de numerieke NHR labels ophaalt als de bijv 0_Nee waarden dus dat die
# dat opsplit en het eerste deel van die string pakt
import pandas as pd
import re
import json
import sys
from nhr_template_creation.nhr_rules_functie import apply_rule
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from excepties.excp_pt3 import prep_df
from openpyxl import load_workbook
import numpy as np
import xlwings as xw

class NHRDataFrame:
    def __init__(self, excel_input_path, excel_output_path, sheet_name):
        self.nhr_data = self._prep_nhr_template(excel_input_path)
        self.excel_output_path = excel_output_path
        self.sheet_name = sheet_name
        self.log = []

    def _prep_nhr_template(self,input_path):
        df = pd.read_excel(input_path, sheet_name= self.sheet_name)
        self.nhr_template = df.copy().drop(
                            columns=['Status', 'Hoeveelheid afgerond',
                                    'ID','Register-ID'],
                            errors='ignore'
                                    )
        postcode_check = r"^\d{4}\s[A-Z]{2}$"
        df["postcode"] = np.where(
            df["postcode"].astype(str).str.match(postcode_check, na=False),
            df["postcode"],
            -1
        )
        df = prep_df(df)

        return df

    def apply_json_rules(self, json_path: str):
        rules = json.loads(Path(json_path).read_text(encoding="utf-8"))
        rules = sorted(rules, key=lambda r: r.get("order", 999))

        for rule in rules:
            mask = apply_rule(self.nhr_data, rule)
            changed = mask.sum()
            self.log.append(f"{rule['name']}: {changed} rows changed")

        return self

    def export_file(self, sheet_name):
        if self.nhr_data is None:
            raise ValueError("Object is leeg")

        output_path = Path(self.excel_output_path)

    # als bestand al bestaat, laad het met openpyxl zodat andere sheets behouden blijven
        if output_path.exists():
            with pd.ExcelWriter(output_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                self.nhr_data.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                self.nhr_data.to_excel(writer, sheet_name=sheet_name, index=False)
            # if self.nhr_data is not None:
            #     self.nhr_data.to_excel(self.excel_output_path, index=False)
            #     print(f"Bestand opgeslagen: {self.excel_output_path}")


