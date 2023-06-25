import os
import sys
import tempfile

from a_pandas_ex_less_memory_more_speed import (
    pd_add_less_memory_more_speed,
    optimize_dtypes,
)
from pandas.api.types import union_categoricals
import gc

pd_add_less_memory_more_speed()
import pandas as pd
from hackyargparser import add_sysargv
from functools import reduce
import pyarrow


@add_sysargv
def convert2parquet(
    csv_file: str | None = None,
    parquet_file: str | None = None,
    chunksize: int = 1000000,
    categorylimit: int = 4,
    verbose: int | bool = 1,
    zerolen_is_na: int | bool = 0,
    *args,
    **kwargs,
) -> None:
    r"""
    The convert2parquet function is used to convert large CSV files into smaller Parquet files.
    It offers several advantages such as reducing memory usage,
    improving processing speed, and optimizing data types for more efficient storage.

    This function might be interesting for individuals or organizations working with large datasets in CSV format
    and looking for ways to optimize their data storage and processing.
    By converting CSV files to Parquet format, which is a columnar storage format, several benefits can be achieved:


    Reduced Memory Usage:

    Parquet files are highly compressed and store data in a columnar format,
    allowing for efficient memory utilization.
    This can significantly reduce the memory footprint compared to traditional row-based CSV files.


    Improved Processing Speed:

    Parquet files are designed for parallel processing and can be read in a highly efficient manner.
    By converting CSV files to Parquet, you can potentially achieve faster data ingestion and query performance.


    Optimized Data Types:

    The function includes a data type optimization step (optimize_dtypes) that aims to minimize the memory usage
    of the resulting Parquet files. It intelligently selects appropriate data types based on the actual
    data values, which can further enhance storage efficiency.

    Categorical Data Optimization:

    The function handles categorical columns efficiently by limiting the number of categories (categorylimit).
    It uses the union_categoricals function to merge categorical data from different chunks,
    reducing duplication and optimizing memory usage.

    Args:
        csv_file (str | None): Path to the input CSV file. Default is None.
        parquet_file (str | None): Path to the output Parquet file. Default is None.
        chunksize (int): Number of rows to read from the CSV file per chunk. Default is 1000000.
        categorylimit (int): The minimum number of categories in categorical columns. Default is 4.
        verbose (int | bool): Verbosity level. Set to 1 or True for verbose output, 0 or False for no output. Default is 1.
        zerolen_is_na (int | bool): Whether to treat zero-length strings as NaN values. Set to 1 or True to enable, 0 or False to disable. Default is 0.
        args: passed to pd.read_csv
        kwargs: passed to pd.read_csv

    Returns:
        None

    Examples:
        # Download the csv:
        https://github.com/hansalemaos/csv2parquet/raw/main/bigcsv.part03.rar
        https://github.com/hansalemaos/csv2parquet/raw/main/bigcsv.part02.rar
        https://github.com/hansalemaos/csv2parquet/raw/main/bigcsv.part01.rar
        # in Python


        from dfcsv2parquet import convert2parquet
        convert2parquet(csv_file=r"C:\bigcsv.csv",
                                        parquet_file=r'c:\parquettest4.pqt',

                                        chunksize=1000000,
                                        categorylimit=4,
                                        verbose=True,
                                        zerolen_is_na=False, )

        # CLI
        python.exe "...\__init__.py" --csv_file "C:\bigcsv.csv" --parquet_file  "c:\parquettest4.pqt" --chunksize 100000 --categorylimit 4 --verbose 1 --zerolen_is_na 1
    """
    allda = []
    verbose = True if verbose else False
    zerolen_is_na = True if zerolen_is_na else False
    for ini, chunk in enumerate(
        pd.read_csv(csv_file, chunksize=chunksize, *args, **kwargs)
    ):
        if verbose:
            print(f"Reading rows: {ini*chunksize} - {(ini+1)*chunksize}")
            print("----------------------------------------------------")
        dftmp = optimize_dtypes(
            dframe=chunk,
            point_zero_to_int=True,
            categorylimit=categorylimit,
            verbose=verbose,
            include_na_strings_in_pd_na=True,
            include_empty_iters_in_pd_na=False,
            include_0_len_string_in_pd_na=zerolen_is_na,
            convert_float=False,
            check_float_difference=False,
        )
        gtmfile = get_tmpfile()
        dftmp.to_parquet(gtmfile)
        allda.append(gtmfile)
        del dftmp
        gc.collect()
    reducecounter = 0

    def joincol(df1, df2):
        nonlocal reducecounter
        reducecounter = reducecounter + 1

        if verbose:
            print(f"Concatenating: {reducecounter}", end="\r")
        if isinstance(df1, str):
            df1 = pd.read_parquet(df1)
        if isinstance(df2, str):
            df2 = pd.read_parquet(df2)

        for col in set(df1.select_dtypes(include="category").columns) & set(
            df2.select_dtypes(include="category").columns
        ):
            uc = union_categoricals([df1[col], df2[col]])
            df1[col] = pd.Categorical(df1[col], categories=uc.categories)
            df2[col] = pd.Categorical(df2[col], categories=uc.categories)
        df3 = pd.concat([df1, df2])
        del df1
        del df2
        del uc
        gc.collect()
        df3.to_parquet(parquet_file)
        del df3
        gc.collect()
        return parquet_file

    _ = reduce(joincol, allda)
    gc.collect()
    for file in allda:
        try:
            os.remove(file)
        except Exception as e:
            print(e)


def get_tmpfile(suffix: str = ".pqt") -> str:
    r"""
    Returns a temporary file path with the specified suffix.

    Args:
        suffix (str): The suffix for the temporary file. Default is ".pmc".

    Returns:
        str: The path to the temporary file.
    """
    tfp = tempfile.NamedTemporaryFile(delete=True, suffix=suffix)
    filename = os.path.normpath(tfp.name)
    tfp.close()
    return filename


if __name__ == "__main__":
    if len(sys.argv) > 1:
        convert2parquet()
