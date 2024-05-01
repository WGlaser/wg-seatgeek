"""_summary_
"""

import json
import math
from typing import List

from helper_functions import replace_blank_dict
from prefect import task
from seatgeek_client import SeatGeek


@task
def create_event_json_file(
    client: SeatGeek,
    performer_by_slug: List[dict[str, str]] | None = None,
    performer_by_id: List[dict[int, str]] | None = None,
    multiple_performers_or: bool | None = None,
    venues: List[dict[str, str, int]] | None = None,
    multiple_venues_or: bool | None = None,
    datetime: dict[str, str] | None = None,
    query: str | None = None,
    taxonomies: List[dict[int, str, int]] | None = None,
    page: int | None = None,
) -> None:
    """_summary_

    Args:
        client (SeatGeek): _description_
        performer_by_slug (List[dict[str, str]] | None, optional): _description_. Defaults to None. # noqa
        performer_by_id (List[dict[int, str]] | None, optional): _description_. Defaults to None. # noqa
        multiple_performers_or (bool | None, optional): _description_. Defaults to None.
        venues (List[dict[str, str, int]] | None, optional): _description_. Defaults to None. # noqa
        multiple_venues_or (bool | None, optional): _description_. Defaults to None.
        datetime (dict[str, str] | None, optional): _description_. Defaults to None.
        query (str | None, optional): _description_. Defaults to None.
        taxonomies (List[dict[int, str, int]] | None, optional): _description_. Defaults to None. # noqa
        page (int | None, optional): _description_. Defaults to None.
    """

    resp = client.get_events(
        performer_by_id=performer_by_id,
        performer_by_slug=performer_by_slug,
        multiple_performers_or=multiple_venues_or,
        venues=venues,
        multiple_venues_or=multiple_performers_or,
        datetime=datetime,
        query=query,
        taxonomies=taxonomies,
        page=page,
    )

    total_pages = math.ceil(resp["meta"]["total"] / resp["meta"]["per_page"])

    results = []

    for item in resp["events"]:
        results.append(item)

    on_page = 2
    while on_page <= total_pages:
        resp = client.get_events(
            performer_by_id=performer_by_id,
            performer_by_slug=performer_by_slug,
            multiple_performers_or=multiple_venues_or,
            venues=venues,
            multiple_venues_or=multiple_performers_or,
            datetime=datetime,
            query=query,
            taxonomies=taxonomies,
            page=on_page,
        )
        for item in resp["events"]:
            results.append(item)
        on_page += 1

    for item in results:
        for key, value in item.items():
            item[key] = replace_blank_dict(value)

    delete_keys = ["playoffs", "contingent", "home_game_number", "game_number"]
    for item in results:
        for bad_key in delete_keys:
            if bad_key in item:
                item.pop(bad_key)

    with open("event.jsonl", "w") as f:
        for entry in results:
            json.dump(entry, f)
            f.write("\n")
