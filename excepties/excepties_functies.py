import pandas as pd
import sys
import warnings
import re

def prep_df(df: pd.DataFrame) -> pd.DataFrame:
    for col in [c for c in df.columns if re.search(r'datum', c, re.IGNORECASE)]:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
        df[col] = df[col].dt.strftime("%d-%m-%Y").fillna("")
    df['logboeknr'] = df['interv_nr'].astype(str).str.replace(r'\D', '', regex=True)
    df['Key'] = (df['pat_nr'].astype(str) + "_" + df['logboeknr'].astype(str)
                        + "_" + df['interv_datum'])
    reorder_cols = ['Index', 'Key', 'logboeknr']
    df = df[reorder_cols + [c for c in df.columns if c not in reorder_cols]]

    return df

def extract_exceptions(df: pd.DataFrame) -> pd.DataFrame:
    # iedere cel wordt een rij door deze cel en bijbehorende kolommen te 'smelten' in de lengte
    melted = df.melt(
        id_vars=[ 'ID','pat_nr', 'interv_nr', 'interv_datum'],
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

    final_path =  sys.argv[2] #r'L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\ablaties\exceptions_df.xlsx'
    result_df.to_excel(final_path,
                           sheet_name='Excepties', index=False)

    print(f"Excepties geladen en opgeslagen: {final_path}")

    return result_df