# SetUp Guide

## Architecture

See `architecture/architecture_diagram` for data flow visualization

## Create S3 Buckets

### Raw Data Bucket

- Create a bucket named `chosen_name-bucket-data`
- Add a folder named `raw/`
- Upload any raw CSV files into here

## Athena Query Results

- Create a new bucket named `athena-query-results`
- This bucket stores all athena data

## Configure IAM Role for Lambda

-  Add AmazonS3FullAccess to the LambdaBasicExecutionRole for the Lambda function

## Create Lambda ETL

### Settings

- Runtime: Python 3.14
- Memory: **512 - 1024 MB**
- Time Out: 15 - 20 seconds

- Place the ETL script into the Lambda console

### Trigger

- Go to the Lambda triggers and add a trigger
- Select S3 and choose the raw bucket
- Event Type is `PUT` with the prefix `raw/ ` to only select the raw data

## Glue Data Catalog

- Add Database and appropriately name it, `etl_db ` was used for this

## Athena Query

- Set output location to the Athena bucket `s3://athena-qresult/`

## Athena → Power BI

- Open ODBC Driver and create a new DSN, ensure output is to the `s3://athena-qresult/`

  ### Load in Power BI

  - Get Data → ODBC → Data Catalog → `etl_db` → table
    
