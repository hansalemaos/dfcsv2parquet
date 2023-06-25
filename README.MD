# converts large CSV files into smaller, Pandas-compatible Parquet files 


## pip install dfcsv2parquet

### Tested against Windows 10 / Python 3.10 / Anaconda 


The convert2parquet function is used to convert large CSV files into smaller Parquet files.
It offers several advantages such as reducing memory usage,
improving processing speed, and optimizing data types for more efficient storage.

This function might be interesting for individuals or organizations working with large datasets in CSV format
and looking for ways to optimize their data storage and processing.
By converting CSV files to Parquet format, which is a columnar storage format, several benefits can be achieved:


### Reduced Memory Usage:

Parquet files are highly compressed and store data in a columnar format,
allowing for efficient memory utilization.
This can significantly reduce the memory footprint compared to traditional row-based CSV files.


### Improved Processing Speed:

Parquet files are designed for parallel processing and can be read in a highly efficient manner.
By converting CSV files to Parquet, you can potentially achieve faster data ingestion and query performance.


### Optimized Data Types:

The function includes a data type optimization step (optimize_dtypes) that aims to minimize the memory usage
of the resulting Parquet files. It intelligently selects appropriate data types based on the actual
data values, which can further enhance storage efficiency.

### Categorical Data Optimization:

The function handles categorical columns efficiently by limiting the number of categories (categorylimit).
It uses the union_categoricals function to merge categorical data from different chunks,
reducing duplication and optimizing memory usage.

```python


        Args:
            csv_file (str | None): Path to the input CSV file. Default is None.
            parquet_file (str | None): Path to the output Parquet file. Default is None.
            chunksize (int): Number of rows to read from the CSV file per chunk. Default is 1000000.
            categorylimit (int): The minimum number of categories in categorical columns. Default is 4.
            verbose (int | bool): Verbosity level. Set to 1 or True for verbose output, 0 or False for no output. Default is 1.
            zerolen_is_na (int | bool): Whether to treat zero-length strings as NaN values. Set to 1 or True to enable, 0 or False to disable. Default is 0.
            args: passed to pd.read_csv (doesn't work with the cli)
            kwargs: passed to pd.read_csv (doesn't work with the cli)

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
```