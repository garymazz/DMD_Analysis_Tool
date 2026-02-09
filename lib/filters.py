from .data_loaders import load_raw_df, set_file_permissions
def get_system_df(input_file, columns, row_start, row_end, err_max, no_header):
    df = load_raw_df(input_file, filter_types=True, no_header=no_header)
    if df is None: return None
    return df
