import pandas as pd
import os
import stat
def load_raw_df(file_path: str, filter_types: bool = True, no_header: bool = False):
    if not os.path.exists(file_path): return None
    header_opt = None if no_header else 0
    try:
        if file_path.endswith('.parquet'): df = pd.read_parquet(file_path)
        elif file_path.endswith('.xlsx'): df = pd.read_excel(file_path, header=header_opt)
        else: df = pd.read_csv(file_path, header=header_opt, low_memory=False)
    except: return None
    if filter_types and 'type' in df.columns: df = df[df['type'] == 'forecast'].copy()
    return df
def set_file_permissions(fp, read_only=True): pass
