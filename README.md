# PAEP Course 03 — Data Engineering

This repository contains unit work, practical applications, and assignments for the third course of the PAEP program. The course is named **Data Engineering and Databases for Artificial Intelligence** in the training materials.

## Course Structure

- Unit 01 — Data Engineering Fundamentals
  - [Student Performance Data Pipeline](unit-01-data-engineering-fundamentals/student-performance-data-pipeline/README.md)

## Current Topics

- Data Engineering fundamentals
- Data lifecycle
- Data ingestion
- Raw and processed storage
- Data cleaning
- Data validation
- Data quality
- ML-ready datasets
- Python and Pandas

## Run the Current Project

From this repository root, change to the project directory:

```powershell
cd unit-01-data-engineering-fundamentals/student-performance-data-pipeline
```

Follow the project README for environment setup. With its local environment available, run:

```powershell
.\.venv\Scripts\python.exe .\src\pipeline.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Raw and processed CSV files are included with the project. Virtual environments, Python caches, generated logs, local environment secrets, and original course PDFs are excluded from Git.
