def upsample(df, upsample_rate, timestamp_col='timestamp', interpolate_method='linear', columns='all'):
    """Upsample a dataframe with a timestamp column.
    :param df: Dataframe to upsample
    :param upsample_rate: Upsample rate in Hz
    :param timestamp_col: Name of the timestamp column
    :param interpolate_method: Interpolation method
    :return: Upsampled dataframe
    """
    if columns == 'all':
        cols = df.columns.tolist()
    else:
        cols = columns
    cols = filter(lambda x: x != 'timestamp', cols)
    data = df.set_index(timestamp_col).resample(f"{1000/upsample_rate}ms").mean().reset_index()
    for col in cols:
        if col != timestamp_col:
            data[col] = data[col].interpolate(method=interpolate_method)
    return data