from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from onetl.connection import SparkHDFS
from onetl.connection import Hive
from onetl.file import FileDFReader
from onetl.file.format import CSV
from onetl.db import DBWriter
from prefect import flow, task

@task
def get_spark():
    return SparkSession.builder.master("yarn").appName("spark-with-yarn").config("spark.sql.warehouse.dir", "/user/hive/warehouse").config("spark.hive.metastore.uris", "thrift://tmpl-jn:9083").enableHiveSupport().getOrCreate()

@task
def stop_spark(spark):
    spark.stop()

@task
def extract(spark):
    hdfs = SparkHDFS(host="tmpl-nn", port=9000, spark=spark, cluster="test")
    reader = FileDFReader(connection=hdfs, format=CSV(delimiter=",", header=True), source_path="/input")
    return reader.run(["mobiles.csv"])

@task
def transform(df):
    return df.orderBy(["Mobile Weight", "RAM"], ascending=[True, False]).filter(df["Company Name"] == "Apple")



@task
def load(df, spark):
    hive = Hive(spark=spark, cluster="test")
    writer = DBWriter(
        connection=hive,
        table="test.spark_partitions",
        options={
            "if_exists": "replace_entire_table",
            "partition_by": ["Company Name"]
        }
    )
    writer.run(df)

@flow
def process_data():
    spark = get_spark()
    df = extract(spark)
    transformed = transform(df)
    load(transformed, spark)
    stop_spark(spark)



if __name__ == "__main__":
    process_data()
