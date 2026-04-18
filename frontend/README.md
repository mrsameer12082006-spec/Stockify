# Ingestion package

This package contains ingestion pipelines for Inventory and Sales data.

Structure:

- sales/: schema, validator, cleaner, pipeline for sales files
- inventory/: schema, validator, cleaner, pipeline for inventory files
- data_uploader.py: helper to load CSV/XLSX into pandas DataFrame
- schema_validator.py, data_cleaner.py: reusable validators/cleaners

Processed files are saved to `ingestion/data/processed/` by the pipeline functions.
# 📥 Data Ingestion & Validation Module  
(Member 2 Contribution)

---

## 📌 Role Overview

As Member 2 of the project, my responsibility was to design and implement the **Data Ingestion & Validation pipeline**.

My module ensures that:

- Uploaded files are properly read
- Data structure is validated
- Data types are enforced
- Missing values are handled
- Duplicate records are removed
- Cleaned dataset is saved for downstream modules

⚠ This module does NOT perform:
- KPI calculation
- Demand forecasting
- Analytics
- Dashboard visualization

It strictly focuses on data preparation.

---

## 🏗 Module Structure

data
|
├──processed
   |
   ├──inventory_cleared.csv

ingestion/
│
├── init.py
├── uploader.py
├── schema.py
├── cleaner.py
└── pipeline.py
├──run_pipeline.py
├──inspect_quality.py
├──sample_inventory.csv


---

## 🔹 uploader.py

### Responsibility:
Reads CSV or Excel files and converts them into a Pandas DataFrame.

### Handles:
- Format detection (.csv / .xlsx)
- File reading errors

This acts as the entry point for raw data.

---

## 🔹 schema.py

### Responsibility:
Validates dataset structure.

### Checks:
- Required column names
- Data type enforcement
- Date parsing for "Last Purchase Date"

If required columns are missing, the module raises a clear error.

This guarantees structural integrity before cleaning.

---

## 🔹 cleaner.py

### Responsibility:
Cleans and standardizes the dataset.

### Operations:
- Removes duplicate rows
- Trims whitespace in string fields
- Fills missing numeric values with 0
- Drops rows missing critical identifiers

Ensures clean and usable dataset output.

---

## 🔹 pipeline.py

### Responsibility:
Orchestrates the ingestion workflow.

### Flow:

1. Load file
2. Validate schema
3. Clean data
4. Save processed dataset

Output file location:

This file is then used by:
- Dashboard module
- Insights module

---

# 🔹 run_pipeline.py (CLI Testing Utility)

### Purpose:
Allows ingestion pipeline to be executed directly from the command line without using Streamlit.

Supports two execution modes:

### Option 1 (Recommended – Module Mode)
bash

python -m ingestion.run_pipeline sample_inventory.csv

---


This file is then used by:
- Dashboard module
- Insights module

---

## 📊 Expected Input Schema

Required columns:

- Product ID
- Product Name
- Category
- Quantity On Hand
- Reorder Point
- Unit Cost
- Selling Price
- Last Purchase Date

Supported formats:
- CSV (.csv)
- Excel (.xlsx)

---

## 🧪 Testing Approach

The module was tested using:

- Valid sample dataset
- Dataset with missing values
- Dataset with duplicate records
- Dataset with missing columns (error test)

The pipeline correctly:
- Raises validation errors
- Cleans invalid entries
- Saves processed dataset

---

## 🧠 Design Principles Followed

- Single Responsibility Principle
- Modular Architecture
- Separation of Concerns
- Clean Error Handling
- Scalable Structure

Each file performs one dedicated task, making the system maintainable and extensible.

---

## 🔗 Integration Instructions

Frontend module should import:

```python
from ingestion import process_inventory_file









