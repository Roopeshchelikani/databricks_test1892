# Databricks notebook source
# MAGIC %run ./neuacc-odp-framework

# COMMAND ----------

import pandas as pd
import os
from pyspark.sql.functions import *

# COMMAND ----------

dbutils.widgets.text(name='metadata_schema', defaultValue='', label='Metadata Schema Name')
dbutils.widgets.text(name='target_catalog', defaultValue='', label='Target UC Catalog')

# COMMAND ----------

# Checking to see if metadata schema is available. Will create it if it does not exists
schema = dbutils.widgets.get('metadata_schema')
target_catalog = dbutils.widgets.get('target_catalog')
full_schema_path = f"{target_catalog}.{schema}"
check_schema(full_schema_path)

# COMMAND ----------

metadata_path = '../../metadata/metadata-files/Databricks'
file_list = os.listdir(metadata_path)

# COMMAND ----------

for sheet in file_list:
  metadata_df = pd.read_csv(f'{metadata_path}/{sheet}')
  delta_df = spark.createDataFrame(metadata_df).write.format('delta').mode('overwrite').option('overwriteSchema','true') \
    .saveAsTable(f"{full_schema_path}.{sheet.replace('.csv','')}")
