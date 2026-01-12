# Sales Analytics System

## Overview
This project implements an end-to-end **Sales Analytics System** using Python.  
It processes raw sales data, performs validation and filtering, enriches transactions
with external API data, and generates a detailed analytics report.

The project is structured as a modular pipeline and satisfies **Assignment 3 – Questions 1 to 6**.

---

## Folder Structure
sales-analytics-system/
│
├── data/
│ └── sales_data.txt
│
├── utils/
│ ├── data_processor.py
│ ├── api_handler.py
│ └── report_generator.py
│
├── output/
│ └── sales_report.txt
│
├── main.py
├── requirements.txt
└── README.md

---

## Requirements
- Python 3.10+
- Internet connection (for API fetch)

Install dependencies:
```bash
pip install -r requirements.txt
How to Run

From the project root directory:
python main.py
You will be prompted to optionally enter:

Minimum transaction amount

Region filter

Press Enter to skip any filter.
Assignment Question Mapping
Question 1 – File Reading & Parsing

Reads sales data from text file

Handles encoding safely

Parses transactions into structured format

Question 2 – Data Validation & Filtering

Validates CustomerID, Region, Quantity, Price

Filters by region and transaction amount

Generates validation summary

Question 3 – Sales Analytics

Region-wise revenue analysis

Top selling products

Customer segmentation based on spend

Question 4 – External API Integration

Fetches product data from public API

Enriches transactions with category, brand, rating

Question 5 – Report Generation

Generates structured text report

Includes region summary, top products, customer segments, peak sales day

Question 6 – Main Application Pipeline

End-to-end CLI-driven workflow

Step-wise execution with progress indicators

Clean final output and report generation
Output

Final report is generated at: output/sales_report.txt
Notes

Code is modular and reusable

All processing steps are logged clearly

Suitable for batch execution and CLI usage
