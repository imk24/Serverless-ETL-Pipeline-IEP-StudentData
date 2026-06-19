CREATE EXTERNAL TABLE etl_db.etl_cleaned (
  name string,
  grade string,
  class string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '\"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://etl-bucket-proj/processed/'
TBLPROPERTIES ('skip.header.line.count' = '1');
