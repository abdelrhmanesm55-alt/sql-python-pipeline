import numpy as np
import pandas as pd
import pyodbc as db

# ---------------------------------------------------------
# 1. Database Connection Configuration
# ---------------------------------------------------------
SERVER = r'WADAA-pc\SQLEXPRESS'
DATABASE = 'test'
CONNECTION_STRING = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    'Trusted_Connection=yes;'
)


def extract_data(conn) -> pd.DataFrame:
    """Extract raw data from Bronze layer."""
    query = 'SELECT * FROM bronze.pipeline_dataset'
    return pd.read_sql(query, conn)


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform the pipeline dataset."""
    df = df.copy()

    # Strip whitespace from text columns
    text_columns = df.select_dtypes(include='object').columns
    for col in text_columns:
        df[col] = df[col].str.strip()

    # Uppercase categorical text columns
    cat_columns = ['department', 'store_region', 'fulfillment_type']
    for col in cat_columns:
        if col in df.columns:
            df[col] = df[col].str.upper()

    # Standardize product code
    df['product_code_new'] = (
        df['product_code']
        .astype(str)
        .str.upper()
        .str.replace('-', '', regex=False)
        .str.replace('_', '', regex=False)
    )

    # Convert order_date and clean format
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    # Data Quality / Validation checks
    df['bad_date'] = df['order_date'].isna()
    df['bad_units'] = df['units_sold'] <= 0
    df['bad_sales'] = df['sales_amount'] <= 0
    df['duplicat_values'] = df.duplicated(subset=['transaction_id'], keep=False)

    # Convert datetime to date object for SQL compatibility
    df['order_date'] = df['order_date'].dt.date

    # Replace NaN with None for SQL NULL execution
    return df.replace({np.nan: None})


def load_data(cursor, df: pd.DataFrame) -> None:
    """Create target table and bulk insert transformed data."""
    create_table_sql = """
    IF OBJECT_ID('pipeline', 'U') IS NOT NULL
        DROP TABLE pipeline;

    CREATE TABLE pipeline (
        transaction_id VARCHAR(50),
        business_id VARCHAR(50),
        order_date DATE,
        product_code VARCHAR(50),
        department VARCHAR(50),
        units_sold INT,
        sales_amount FLOAT,
        store_region VARCHAR(50),
        fulfillment_type VARCHAR(50),
        warehouse VARCHAR(50),
        product_code_new VARCHAR(50),
        bad_date BIT,
        bad_units BIT,
        bad_sales BIT,
        duplicat_values BIT
    );
    """
    cursor.execute(create_table_sql)

    insert_sql = """
        INSERT INTO pipeline
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    rows = list(df.itertuples(index=False, name=None))
    cursor.executemany(insert_sql, rows)
    print(f" Successfully inserted {len(rows)} rows into 'pipeline' table.")


# ---------------------------------------------------------
# Main Execution Flow
# ---------------------------------------------------------
def main():
    try:
        with db.connect(CONNECTION_STRING, autocommit=True) as conn:
            cursor = conn.cursor()
            cursor.fast_executemany = True

            print("Extracting data...")
            raw_df = extract_data(conn)

            print("Transforming data...")
            cleaned_df = transform_data(raw_df)

            print("Loading data...")
            load_data(cursor, cleaned_df)

    except Exception as e:
        print(f" An error occurred during pipeline execution: {e}")


if __name__ == '__main__':
    main()
