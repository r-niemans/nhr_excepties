import pandas as pd
import sys
import warnings
import re
import xlwings as xw

"""
DIT SCRIPT MOET N0G GETEST WORDEN; incrementeel laden in bestaande excel workbook
"""

def prep_df(df: pd.DataFrame) -> pd.DataFrame:
    for col in [c for c in df.columns if re.search(r'datum', c, re.IGNORECASE)]:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
        df[col] = df[col].dt.strftime("%d-%m-%Y").fillna("")
    df['logboeknr'] = df['interv_nr'].astype(str).str.replace(r'\D', '', regex=True)
    df['Key'] = (df['pat_nr'].astype(str) + "_" + df['logboeknr'].astype(str)
                        + "_" + df['interv_datum'])
    reorder_cols = ['Key', 'logboeknr']
    df = df[reorder_cols + [c for c in df.columns if c not in reorder_cols]]

    return df

def extract_exceptions(df: pd.DataFrame) -> pd.DataFrame:
    # iedere cel wordt een rij door deze cel en bijbehorende kolommen te 'smelten' in de lengte
    melted = df.melt(
        id_vars=['pat_nr', 'interv_nr', 'interv_datum'],
        value_vars=df.columns,
        var_name='NHR_item',
        value_name='Origineel_resultaat'
    )

    excepties_rows = melted['Origineel_resultaat'].isin([-1, '-1'])
    result_df = melted[excepties_rows].copy()
    result_df = prep_df(result_df)
    result_df['IDvLookup'] = result_df['interv_nr'].astype(str) + "_" + result_df['NHR_item']
    result_df['Definitief_resultaat'] = ''
    result_df['Antwoord_mogelijkheden'] = ''
    result_df['Opmerking'] = ''

    if not -1 in result_df['Origineel_resultaat'] or '-1' in result_df['Origineel_resultaat']:
        warnings.warn("Andere exceptiewaarde dan -1")

    #juiste kolomvolgorde
    result_df = result_df[[
                        'Key', 'logboeknr','interv_nr', 'interv_datum',
                        'pat_nr', 'IDvLookup', 'NHR_item', 'Origineel_resultaat',
                        'Definitief_resultaat', 'Antwoord_mogelijkheden', 'Opmerking'
                        ]]

    # check of de kolommen uniek zijn
    unique_check = result_df['IDvLookup'].is_unique
    if not unique_check is True:
        raise Exception("Pas op: IDvLookup is niet uniek")

    final_path =  sys.argv[1] #r'L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\ablaties\exceptions_df.xlsx'
    result_df.to_excel(final_path,
                           sheet_name='Excepties', index=False) #sheet name dynamisch maken? dat obv user input die waarde daar wordt gezet

    sheet_name = 'Excepties'
    key_col = 'IDvLookup'
    app = xw.App(visible=False)
    wb = xw.Book(final_path)

    # Controleer of doel-sheet bestaat, anders aanmaken
    if sheet_name in [sheet.name for sheet in wb.sheets]:
        sheet = wb.sheets[sheet_name]
    else:
        sheet = wb.sheets.add(sheet_name)

    used_range = sheet.used_range
    data = used_range.value

    if data and len(data) > 1:
        headers = data[0]
        existing_df = pd.DataFrame(data[1:], columns=headers).dropna(how="all")
    else:
        existing_df = pd.DataFrame(columns=result_df.columns)

    # Vind nieuwe rijen die nog niet bestaan
    if key_col in result_df.columns and key_col in existing_df.columns:
        new_rows = result_df[~result_df[key_col].isin(existing_df[key_col])]
    else:
        # Als key niet bestaat, voeg alles toe
        new_rows = result_df.copy()

    # Indien key mist of leeg is, genereer nieuwe ID’s
    if key_col in new_rows.columns and new_rows[key_col].isnull().any():
        max_id = existing_df[key_col].max() if not existing_df.empty else 0
        new_rows[key_col] = range(max_id + 1, max_id + 1 + len(new_rows))

    # Voeg de nieuwe rijen toe onder de bestaande
    if not new_rows.empty:
        start_row = len(existing_df) + 2  # +1 header, +1 indexering
        sheet.range(f"A{start_row}").value = new_rows.values.tolist()
        print(f" {len(new_rows)} nieuwe rijen toegevoegd aan '{sheet_name}'")
    else:
        print("Geen nieuwe rijen om toe te voegen.")

    wb.save()
    wb.close()
    app.quit()

    print(f"Excepties geladen en opgeslagen: {final_path}")

    return result_df