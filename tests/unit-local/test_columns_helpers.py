import os
import pytest

from chispa.dataframe_comparer import *
from databricks.connect import DatabricksSession as SparkSession
from databricks.sdk import WorkspaceClient

from helpers.columns_helpers import *


@pytest.fixture(scope="session")
def spark_session() -> SparkSession:

    # Wait for the spark session to be created, otherwise the following error occurs:
    # pyspark.errors.exceptions.connect.SparkConnectGrpcException:
    # (org.apache.spark.SparkSQLException) [INVALID_HANDLE.SESSION_NOT_FOUND]
    # The handle 8f333dc3-8476-4663-afce-4c582571ceac is invalid. Session not found. SQLSTATE: HY000
    w = WorkspaceClient()

    cluster_id = os.environ["TEST_CLUSTER_ID"]
    w.clusters.ensure_cluster_is_running(cluster_id)

    spark = SparkSession.builder.getOrCreate()
    return spark


def test_columns_except(spark_session: SparkSession):
    original_df = spark_session.createDataFrame(
        [[1, 2, 3, 4]], schema="col1 int, col2 int, col3 int, col4 int"
    )
    new_cols = columns_except(original_df, ["col2", "col4"])
    assert new_cols == ["col1", "col3"]


def test_dataframe_except_columns(spark_session: SparkSession):
    original_df = spark_session.createDataFrame(
        [[1, 2, 3, 4]], schema="col1 int, col2 int, col3 int, col4 int"
    )
    new_df = dataframe_except_columns(original_df, ["col2", "col4"])
    expected_df = spark_session.createDataFrame([[1, 3]], schema="col1 int, col3 int")
    assert_df_equality(new_df, expected_df, ignore_nullable=True)


def test_add_missing_columns(spark_session: SparkSession):
    df1 = spark_session.createDataFrame([[1, 2]], schema="col1 int, col2 int")
    df2 = spark_session.createDataFrame(
        [[1, "2", 3.0]], schema="col1 int, col4 string, col5 double"
    )
    new_df = add_missing_columns(df1, df2)
    expected_df = spark_session.createDataFrame(
        [[1, 2, None, None]], schema="col1 int, col2 int, col4 string, col5 double"
    )
    assert_df_equality(new_df, expected_df, ignore_nullable=True)
