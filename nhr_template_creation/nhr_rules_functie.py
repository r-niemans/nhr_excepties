
import operator as ops
import pandas as pd
from typing import Dict, Callable
import numpy as np

def apply_rule(df: pd.DataFrame, rule: Dict) -> pd.Series:
    ops_map = {"==": ops.eq, "!=": ops.ne}
    mask = pd.Series(True, index=df.index)

    for cond in rule.get("lookup_conditions", []):
        col = cond["col"]
        comparison = cond["comparison"]
        vals = cond["values"]

        if comparison not in ops_map or col not in df.columns:
            continue
        if not isinstance(vals, list):
            vals = [vals]

        func: Callable = ops_map[comparison]

        col_data = df[col]
        if not pd.api.types.is_numeric_dtype(col_data):
            col_series = col_data.astype(str).str.split("_").str[0]
        else:
            col_series = col_data

        col_series = pd.to_numeric(col_series, errors="coerce")

        col_mask = pd.Series(False, index=df.index)
        for v in vals:
            try:
                v = int(v)
            except Exception(TypeError):
                pass
            col_mask |= func(col_series, v)

        mask &= col_mask

    if "future_value" not in rule or rule["future_value"] is None:
        return mask

    fv = rule["future_value"]

    for col in rule["cols_to_change"]:
        current_dtype = df[col].dtype

        # case 1: numeric column + numeric value
        if pd.api.types.is_numeric_dtype(current_dtype) and isinstance(fv, (int, float, np.number)):
            df.loc[mask, col] = np.float64(fv)

        # case 2: numeric column + string future value (e.g. "")
        elif pd.api.types.is_numeric_dtype(current_dtype) and isinstance(fv, str):
            df[col] = df[col].astype("object")
            df.loc[mask, col] = fv


        else:
            df.loc[mask, col] = fv

    return mask

