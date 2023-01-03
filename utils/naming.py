import re

def to_snake_case(name):
    """Converts a string to snake case.

    Args:
        name (str): The string to convert.

    Returns:
        str: The converted string.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return re.sub('_+', '_', s2)

def standardize_column_names(df, inplace=False, columns='all'):
    """Standardizes column names to snake case.

    Args:
        df (pandas.DataFrame): dataframe to standardize column names
        inplace (bool, optional): defaults to False
        columns (str or list, optional): defaults to 'all'

    Raises:
        TypeError: columns must be a list of strings or "all"

    Returns:
        pandas.DataFrame: dataframe with standardized column names
    """
    if columns == 'all':
        columns = df.columns
    if type(columns) == list:
        raise TypeError('columns must be a list of strings or "all"')
    df = df.rename(columns={old: to_snake_case(old) for old in df.columns}, inplace=inplace)
    return df