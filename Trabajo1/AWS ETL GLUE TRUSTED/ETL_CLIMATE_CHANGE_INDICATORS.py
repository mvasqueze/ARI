import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Read data from S3
data = glueContext.create_dynamic_frame.from_catalog(
    database="rawtotrusteddb",
    table_name="climate_change_indicators_83cc632aa7b85365d4cd8a18b81dc435",
    transformation_ctx="data"
)

# Write data to Trusted zone in Parquet format
sink = glueContext.getSink(
    path="s3://climate-change-datalake/Trusted/climate_change_indicators/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="sink"
)
sink.setCatalogInfo(
    catalogDatabase="rawtotrusteddb",
    catalogTableName="climate_change_indicators_trusted"
)
sink.setFormat("glueparquet", compression="snappy")
sink.writeFrame(data)
job.commit()
