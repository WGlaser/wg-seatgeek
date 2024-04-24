"""
Prefect tasks for conveniently interacting with BigQuery.
"""

from google.cloud.bigquery import Client, Dataset
from google.cloud.exceptions import Conflict
from prefect import get_run_logger, task
from prefect_gcp import GcpCredentials


@task
def create_bigquery_dataset(
    gcp_credentials: GcpCredentials, dataset_name: str
) -> Dataset:
    """Creates a dataset in BigQuery if it doesn't already exist.

    Args:
        gcp_credentials (GcpCredentials): a Prefect GcpCredentials block
        dataset_name (str): the name of the dataset to create

    Returns:
        Dataset: the created dataset
    """
    logger = get_run_logger()

    client: Client = gcp_credentials.get_bigquery_client()
    dataset = Dataset(f"{client.project}.{dataset_name}")
    dataset.location = "US"
    try:
        dataset = client.create_dataset(dataset=dataset)
    except Conflict as e:
        logger.warning(e)
        dataset = client.get_dataset(dataset)
        logger.warning(
            f"Dataset `{dataset.dataset_id}` already exists. Skipping dataset creation."
        )
    else:
        logger.info(f"Dataset {dataset.dataset_id} created")

    return dataset
