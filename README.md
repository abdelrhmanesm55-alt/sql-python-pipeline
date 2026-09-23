# SQL-Python ETL Data Pipeline

---

### 📌 Overview
This project demonstrates an **End-to-End ETL (Extract, Transform, Load) Pipeline** built with **Python** and **SQL Server**. 

The pipeline extracts raw e-commerce transaction data from a **Bronze Layer** inside SQL Server, cleans and validates the dataset using Python (`pandas`), applies data quality checks, and loads the structured data into a target SQL pipeline table.

---

### 🏗️ Architecture & Workflow

1. **Bronze Layer (Ingestion):** 
   - Load raw `pipeline_dataset.csv` into SQL Server (`bronze.pipeline_dataset`) using T-SQL `BULK INSERT`.
2. **Transform (Python Execution):**
   - **Text Standardization:** Trim whitespace and convert categorical columns (`department`, `store_region`, `fulfillment_type`) to uppercase.
   - **Product Code Normalization:** Strip symbols (`-`, `_`) and force uppercase formatting.
   - **Data Quality Auditing:** Flag records with missing dates (`bad_date`), non-positive units (`bad_units`), non-positive sales (`bad_sales`), or duplicate transaction IDs (`duplicat_values`).
3. **Load (Target Storage):**
   - Re-create the target `pipeline` table in SQL Server and perform high-performance bulk insertions via `pyodbc` (`fast_executemany = True`).

---

### 📁 Project Structure

```text
sql-python-pipeline/
│
├── schema.sql           # T-SQL script to create Bronze schema & bulk insert CSV
├── pipeline.py          # Main Python script executing the ETL workflow
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

----

### 🚀 Getting Started
- SQL Server (with ODBC Driver 17 installed)
- Python 3.8+

----

### Installation & Setup
1- Clone the Repository:
      git clone [https://github.com/YOUR_USERNAME/sql-python-pipeline.git](https://github.com/YOUR_USERNAME/sql-python-pipeline.git)
      cd sql-python-pipeline

2-Install Dependencies:
      pip install -r requirements.txt

3- Setup Bronze Layer in SQL Server:
    - Execute the SQL queries inside (schema.sql) in SQL Server Management Studio (SSMS).
    - Note: Update the file path in (BULK INSERT) to point to your local CSV path.

4- Run the Pipeline:
    python pipeline.py
