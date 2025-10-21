# gebruik ofwel mijn oude script of maak een class aan waar alle rules instaan
# die dan aangeroepen kunnen worden
# !!! zorg dat mijn script zowel de numerieke NHR labels ophaalt als de bijv 0_Nee waarden dus dat die
# dat opsplit en het eerste deel van die string pakt
import pandas as pd
import re
import json
from nhr_rules_functie import apply_rule
from excepties.excepties_functies import prep_df
from pathlib import Path
import numpy as np
import xlwings as xw

class NHRDataFrame:
    def __init__(self, excel_input_path, excel_output_path):
        self.nhr_data = self._prep_nhr_template(excel_input_path)
        self.excel_output_path = excel_output_path
        self.log = []

    def _prep_nhr_template(self,input_path):
        df = pd.read_excel(input_path, sheet_name="ABL_NHR")
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

    def export_file(self):
        excel_template_path = r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\ablaties\ABL_Epic_Verrichtingen_CAR.xlsx"
        if self.nhr_data is not None:
                wb = xw.Book(excel_template_path)
                sheet_name = 'ABL NHR Template'
                if sheet_name in [sheet.name for sheet in wb.sheets]:
                    sheet = wb.sheets[sheet_name]
                else:
                    sheet = wb.sheets.add(sheet_name)  # voeg sheet toe, als die niet bestaat

                sheet.range("A2").value = self.nhr_data

                wb.save()
                wb.close()
       # if self.nhr_data is not None:
       #     self.nhr_data.to_excel(self.excel_output_path, index=False)
       #     print(f"Bestand opgeslagen: {self.excel_output_path}")
        else:
            raise ValueError("Object is leeg")

