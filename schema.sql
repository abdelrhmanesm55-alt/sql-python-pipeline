-- 1. Make sure there is a Schema named bronze
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'bronze')
BEGIN
    EXEC('CREATE SCHEMA bronze');
END
GO

-- 2. Delete the old table if it exists and recreate it.
IF OBJECT_ID('bronze.pipeline_dataset', 'U') IS NOT NULL
    DROP TABLE bronze.pipeline_dataset;
GO

CREATE TABLE bronze.pipeline_dataset (
    transaction_id   VARCHAR(50),
    business_id      VARCHAR(50),
    order_date       VARCHAR(50),
    product_code     VARCHAR(50),
    department       VARCHAR(50),
    units_sold       INT,
    sales_amount     FLOAT,
    store_region     VARCHAR(50),
    fulfillment_type VARCHAR(50),
    warehouse        VARCHAR(50)
);
GO

-- 3. Importing data from a CSV file
BULK INSERT bronze.pipeline_dataset
FROM 'C:\Users\Techno Shield\Downloads\pipeline_dataset.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);
GO

-- 4. Data access verification
SELECT TOP 10 * FROM bronze.pipeline_dataset;
