# AWS Serverless IEP ETL Pipeline

This project is an end-to-end, serverless ETL pipeline on AWS that ingests, transforms, and analyzes anonymized IEP (Individualized Education Program) student data. It uses event-driven automation with S3 and AWS Lambda, and exposes the processed data through Athena and Power BI for analytics and reporting.

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
