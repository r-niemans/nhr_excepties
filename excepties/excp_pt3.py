import pandas as pd
import xlwings as xw
import warnings
import re


def prep_df(df: pd.DataFrame) -> pd.DataFrame:
    for col in [c for c in df.columns if re.search(r'datum', c, re.IGNORECASE)]:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
        df[col] = df[col].dt.strftime("%d-%m-%Y").fillna("")
    df['logboeknr'] = df['interv_nr'].astype(str).str.replace(r'\D', '', regex=True)
    df['Key'] = (
        df['pat_nr'].astype(str)
        + "_"
        + df['logboeknr'].astype(str)
        + "_"
        + df['interv_datum']
    )
    reorder_cols = ['Key', 'logboeknr']
    df = df[reorder_cols + [c for c in df.columns if c not in reorder_cols]]
    return df


def extract_exceptions_incremental(
    df: pd.DataFrame,
    existing_wb_path: str,
    sheet_name: str = "Excepties",
    separate_export_path: str | None = None,
) -> pd.DataFrame:
    """Extract rows where Origineel_resultaat == -1, process via prep_df, and incrementally
    append to an existing Excel sheet without overwriting or duplicates."""

    id_cols = ['pat_nr', 'interv_nr', 'interv_datum']
    missing = [c for c in id_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Input df missing required id columns: {missing}")

    # Melt only the non-ID columns
    value_cols = [c for c in df.columns if c not in id_cols]
    melted = df.melt(
        id_vars=id_cols,
        value_vars=value_cols,
        var_name='NHR_item',
        value_name='Origineel_resultaat'
    )

    # Filter only rows with -1
    is_exception = melted['Origineel_resultaat'].isin([-1, "-1"])
    result_df = melted.loc[is_exception].copy()

    if result_df.empty:
        print("Geen -1 excepties gevonden.")
        return pd.DataFrame()

    # Warn if other negative values exist
    others = melted.loc[~is_exception & melted['Origineel_resultaat'].notna()]
    if not others.empty and (others['Origineel_resultaat'].astype(str).str.startswith('-').any()):
        warnings.warn("Andere exceptiewaarde dan -1 gedetecteerd (genegeerd).")

    # --- Apply your prep_df function ---
    result_df = prep_df(result_df)

    # Build IDvLookup and ensure correct structure
    result_df['IDvLookup'] = result_df['interv_nr'].astype(str) + "_" + result_df['NHR_item']
    for col in ['Definitief_resultaat', 'Antwoord_mogelijkheden', 'Opmerking']:
        if col not in result_df.columns:
            result_df[col] = ''

    desired_cols = [
        'Key', 'logboeknr', 'interv_nr', 'interv_datum',
        'pat_nr', 'IDvLookup', 'NHR_item', 'Origineel_resultaat',
        'Definitief_resultaat', 'Antwoord_mogelijkheden', 'Opmerking'
    ]
    result_df = result_df[[c for c in desired_cols if c in result_df.columns]]

    # --- Incremental append logic ---
    app = xw.App(visible=False, add_book=False)
    try:
        wb = xw.Book(existing_wb_path)
        if sheet_name in [s.name for s in wb.sheets]:
            sheet = wb.sheets[sheet_name]
        else:
            sheet = wb.sheets.add(sheet_name)

        used = sheet.used_range
        data = used.value

        if data and len(data) > 1:
            headers = data[0]
            existing_df = pd.DataFrame(data[1:], columns=headers).dropna(how="all")
        elif data and len(data) == 1:
            existing_df = pd.DataFrame(columns=data[0])
        else:
            existing_df = pd.DataFrame(columns=result_df.columns)

        # Align and deduplicate by IDvLookup
        for col in result_df.columns:
            if col not in existing_df.columns:
                existing_df[col] = ''
        for col in existing_df.columns:
            if col not in result_df.columns:
                result_df[col] = ''

        key_col = 'IDvLookup'
        if key_col in existing_df.columns:
            new_rows = result_df[~result_df[key_col].isin(existing_df[key_col])]
        else:
            new_rows = result_df.copy()

        if not new_rows.empty:
            combined = pd.concat([existing_df, new_rows], ignore_index=True)
            if not combined[key_col].is_unique:
                raise Exception("IDvLookup niet uniek na samenvoegen.")

            sheet.clear()
            sheet["A1"].value = combined
            print(f"{len(new_rows)} nieuwe rijen toegevoegd aan '{sheet_name}'.")
        else:
            print("Geen nieuwe rijen om toe te voegen.")

        wb.save()
        wb.close()
    finally:
        app.quit()

    # --- Optional separate export ---
    if separate_export_path:
        result_df.to_excel(separate_export_path, sheet_name='Excepties', index=False)

    print(f"Excepties verwerkt en opgeslagen in: {existing_wb_path}")
    return result_df
