"""
Prefect flow for use with seatgeek-client
"""
from datetime import date

from anyio import run
from credentials import SeatGeekCredentials
from prefect import flow
from prefect.variables import Variable
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import cloud_storage_upload_blob_from_file
from seatgeek_client import SeatGeek

# from tasks.bigquery import create_bigquery_dataset
from tasks.events import create_event_json_file
from tasks.gcs import create_gcs_bucket

DATASET = "SeatGeek"


@flow
async def wg_seatgeek(
    performer_by_slug: list[dict] | None = None,
    performer_by_id: list[dict] | None = None,
    multiple_performers_or: bool | None = None,
    venues: list[dict] | None = None,
    multiple_venues_or: bool | None = None,
    datetime: dict | None = None,
    query: str | None = None,
    taxonomies: list[dict] | None = None,
) -> None:
    """_summary_

    Args:
        performer_by_slug (List[dict[str, str]] | None, optional): _description_. Defaults to None. # noqa
        performer_by_id (List[dict[int, str]] | None, optional): _description_. Defaults to None. # noqa
        multiple_performers_or (bool | None, optional): _description_. Defaults to None.
        venues (List[dict[str, str, int]] | None, optional): _description_. Defaults to None. # noqa
        multiple_venues_or (bool | None, optional): _description_. Defaults to None.
        datetime (dict[str, str] | None, optional): _description_. Defaults to None.
        query (str | None, optional): _description_. Defaults to None.
        taxonomies (List[dict[int, str, int]] | None, optional): _description_. Defaults to None. # noqa
    """
    text = await Variable.get("gcp_block_name")
    print(text.value)
    gcp_credentials_block: GcpCredentials = await GcpCredentials.load(text.value)
    seatgeek_credentials_block: SeatGeekCredentials = await SeatGeekCredentials.load(
        "seatgeek-credentials"
    )
    bucket_name = "seatgeek-data"

    create_gcs_bucket(gcp_credentials=gcp_credentials_block, bucket_name=bucket_name)

    client = SeatGeek(
        seatgeek_credentials_block.key,
        seatgeek_credentials_block.secret.get_secret_value(),
    )
    create_event_json_file(
        client=client,
        performer_by_id=performer_by_id,
        performer_by_slug=performer_by_slug,
        multiple_performers_or=multiple_venues_or,
        venues=venues,
        multiple_venues_or=multiple_performers_or,
        datetime=datetime,
        query=query,
        taxonomies=taxonomies,
        page=1,
    )

    # gcp_bucket: GcsBucket = GcsBucket.load(bucket_name)
    today = date.today()
    await cloud_storage_upload_blob_from_file(
        file="event.jsonl",
        bucket=bucket_name,
        blob=f"events/{today:%Y}/{today:%m}/{today:%d}/report.json",
        gcp_credentials=gcp_credentials_block,
    )


if __name__ == "__main__":
    run(wg_seatgeek, [{"slug": "Boston-Celtics", "specificity": "home_team"}])
