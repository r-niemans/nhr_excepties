import operator as ops
import pandas as pd
from typing import List, Dict, Union, Callable

def apply_rule(df: pd.DataFrame, rule: Dict) -> pd.Series:
    ops_map = {
        "==": ops.eq,
        "!=": ops.ne,
    }

    # EN-conditie over alle lookup_conditions
    mask = pd.Series(True, index=df.index)

    for cond in rule["lookup_conditions"]:
        col = cond["col"]
        comparison = cond["comparison"]
        vals = cond["values"]
        if not isinstance(vals, list):
            vals = [vals]
        func: Callable = ops_map[comparison]

        col_mask = pd.Series(False, index=df.index)
        for v in vals:
            col_mask = col_mask | func(df[col], v)

        mask = mask & col_mask  # EN-combinatie van alle voorwaarden

    # Pas de waarde toe op de target-kolommen, bijvoorbeeld cols_to_change: kath_ablatieAT=0 DAN future_value : klinische_setting_AT= ""
    df.loc[mask, rule["cols_to_change"]] = rule["future_value"]

    return mask
