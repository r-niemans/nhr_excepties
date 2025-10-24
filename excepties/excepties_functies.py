import re
import traceback
import warnings
import pandas as pd
import xlwings as xw


def prep_df(df: pd.DataFrame) -> pd.DataFrame:
    for col in [c for c in df.columns if re.search(r'datum', c, re.IGNORECASE)]:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
        df[col] = df[col].dt.strftime("%d-%m-%Y").fillna("")
    df["logboeknr"] = df["interv_nr"].astype(str).str.replace(r"\D", "", regex=True)
    df["Key"] = (
        df["pat_nr"].astype(str)
        + "_"
        + df["logboeknr"].astype(str)
        + "_"
        + df["interv_datum"]
    )
    reorder_cols = ["Key", "logboeknr"]
    df = df[reorder_cols + [c for c in df.columns if c not in reorder_cols]]
    return df

def extract_exceptions_incremental(
    df: pd.DataFrame,
    existing_wb_path: str,
    sheet_name: str = "Excepties",
) -> pd.DataFrame:

    id_cols = ["pat_nr", "interv_nr", "interv_datum"]
    missing = [c for c in id_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Input df mist kolom: {missing}")

    value_cols = [c for c in df.columns if c not in id_cols]
    melted = df.melt(
        id_vars=id_cols,
        value_vars=value_cols,
        var_name="NHR_item",
        value_name="Origineel_resultaat",
    )

    # Haal -1 waarden eruit
    is_exception = melted["Origineel_resultaat"].isin([-1, "-1"])
    result_df = melted.loc[is_exception].copy()

    if result_df.empty:
        print("Geen -1 excepties gevonden.")
        return pd.DataFrame()

    result_df = prep_df(result_df)
    result_df["ID vLookup"] = result_df["interv_nr"].astype(str) + "_" + result_df["NHR_item"]

    for col in ["Definitief_resultaat", "Antwoord_mogelijkheden", "Opmerking"]:
        if col not in result_df.columns:
            result_df[col] = ""

    desired_cols = [
        "Key", "logboeknr", "interv_nr", "interv_datum",
        "pat_nr", "ID vLookup", "NHR_item", "Origineel_resultaat",
        "Definitief_resultaat", "Antwoord_mogelijkheden", "Opmerking"
    ]
    result_df = result_df[desired_cols]

    try:
        existing_df = pd.read_excel(existing_wb_path, sheet_name=sheet_name)
    except Exception(BaseException):
        print("Lege/ongeldige Excepties-sheet, maak nieuwe structuur aan.")
        existing_df = pd.DataFrame(columns=result_df.columns)

    for col in result_df.columns:
        if col not in existing_df.columns:
            existing_df[col] = ""
    for col in existing_df.columns:
        if col not in result_df.columns:
            result_df[col] = ""

    key_col = "ID vLookup"
    if key_col in existing_df.columns:
        new_rows = result_df[~result_df[key_col].isin(existing_df[key_col])]
    else:
        new_rows = result_df.copy()

    if not new_rows.empty:
        all_cols = sorted(set(existing_df.columns).union(new_rows.columns))
        existing_df = existing_df.reindex(columns=all_cols, fill_value="")
        new_rows = new_rows.reindex(columns=all_cols, fill_value="")
        combined = pd.concat([existing_df, new_rows], ignore_index=True)

        # dubbele ID's verwijderen
        if not combined["ID vLookup"].is_unique:
            dupes = combined.loc[combined["ID vLookup"].duplicated(), "ID vLookup"].unique()
            warnings.warn(
                f"{len(dupes)} dubbele ID vLookup-waarden gevonden! "
            )

        with pd.ExcelWriter(existing_wb_path, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            combined.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"{len(new_rows)} nieuwe rijen toegevoegd aan '{sheet_name}'.")
    else:
        print("Geen nieuwe rijen om toe te voegen.")
    return result_df
