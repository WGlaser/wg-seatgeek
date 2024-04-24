"""_summary_

"""

from google.cloud.exceptions import Conflict
from prefect import get_run_logger, task
from prefect_gcp import GcpCredentials, GcsBucket


@task
def create_gcs_bucket(gcp_credentials: GcpCredentials, bucket_name: str) -> GcsBucket:
    """Create a GCS bucket if it doesn't already exist.

    Args:
        gcp_credentials (GcpCredentials): a Prefect GcpCredentials block
        bucket_name (str): the name of the bucket to create

    Returns:
        GcsBucket: a GcsBucket Prefect block
    """
    logger = get_run_logger()

    gcs_bucket = GcsBucket(
        bucket=bucket_name,
        gcp_credentials=gcp_credentials,
    )

    try:
        gcs_bucket.create_bucket()
    except Conflict as e:
        logger.warning(e)
        logger.warning(
            f"Bucket `{bucket_name}` already exists. Skipping bucket creation."
        )

    return gcs_bucket
