# Overview

This repository documents an end‑to‑end, serverless ETL pipeline built on Amazon Web Services to ingest, clean, and transform raw IEP (Individualized Education Program) student data. The pipeline automates data processing using S3 event triggers and AWS Lambda, stores cleaned outputs in S3, and exposes the processed dataset through Athena for analysis and visualization in Power BI.

The project demonstrates how cloud‑native, event‑driven architecture can streamline data workflows while maintaining strict privacy controls through anonymized, codename‑based student identifiers.

## Objective

 - The primary objective of this project was to support a local elementary school in organizing, analyzing, and acting on IEP-related student data through a scalable, serverless cloud environment.
- By integrating Athena with Power BI, the solution enabled stakeholders to visualize key trends such as subject-specific support and instructional workload distribution through interactive dashboards.
- The automated ETL workflow reduced manual data preparation and cleaning efforts, allowing staff to spend less time managing spreadsheets and more time making data-informed decisions.  

## Architecture

- **Storage:** Amazon S3 (raw + processed data)
- **Compute / ETL:** AWS Lambda (Python + Pandas)
- **Metadata:** AWS Glue Data Catalog
- **Query Engine:** Amazon Athena
- **BI / Dashboards:** Power BI via ODBC + Import
Full Breakdown is in `architecture/architecture_diagram`

### Workflow + Concepts

1. **Raw data upload** → dropped into an S3 `raw/` bucket.
2. **S3 event notification** → triggers a Lambda ETL function.
3. **Lambda ETL** → performs:
   - Deduplication
   - Schema normalization (consistent column names, types, formats)
   - O(1) teacher–student lookup using dictionary-based mapping
4. **Processed data** → written to S3 `processed/` bucket.
5. **Glue Data Catalog** → registers tables over processed data.
6. **Athena** → runs serverless SQL queries over Glue tables.
7. **Power BI** → connects to Athena for interactive dashboards.

## Features

- **Fully serverless:** No provisioned servers; pay-per-use via Lambda and Athena.
- **Event-driven:** S3 uploads automatically trigger ETL runs.
- **Data quality:** Python/Pandas cleaning logic improves consistency and reliability.
- **Analytics-ready:** Glue + Athena provide structured, queryable datasets.
- **Privacy-aware:** All data is self-generated and anonymized using coded identifiers.

## Tech stack

- **AWS:** S3, Lambda, Glue, Athena, IAM
- **Language:** Python 3.14
- **Libraries:** Pandas, boto3
- **BI** Power BI Import + ODBC driver

## Getting Started

- Upload raw CSV files to the `raw/` S3 bucket
- Lambda ETL is triggered and processes and writes the cleaned data to `processed/` automatically
- Athena queries the processed dataset through external tables
- Power BI connects via ODBC for visualizations
Detailed setup instructions are in `docs/setup_guide.md`
