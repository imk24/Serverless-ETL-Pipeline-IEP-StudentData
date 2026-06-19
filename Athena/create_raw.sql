CREATE EXTERNAL TABLE IF NOT EXISTS etl_db.raw_iep_data (
    role        string,
    grade       int,
    name        string,
    class       string,
    minutes     string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
     'separatorChar' = ',',
    'quoteChar' = '\"',
    'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://etl-bucket-proj/raw/'
TBLPROPERTIES ('skip.header.line.count'='1');
