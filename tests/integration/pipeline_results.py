# Databricks notebook source
# This notebook defines tests for DLT pipeline

# COMMAND ----------

schema = dbutils.widgets.get("schema")
test_table = f"{schema}.clickstream_filtered"
print(f"Testing table: {test_table}")

# COMMAND ----------
print("Check number of records")
cnt = spark.table(test_table).count()
assert cnt == 12480649

# COMMAND ----------

print("Check types")
values = spark.table(test_table).select("type").distinct().collect()
values_list = [val["type"] for val in values]
VALID_VALUES = ["link", "redlink"]

print(f"Types found: {values_list}")

for val in values_list:
    assert val in VALID_VALUES
