"""
Prefect flow for use with seatgeek-client
"""
from anyio import run
from prefect import flow, get_run_logger


@flow
async def wg_seatgeek(team: str) -> None:
    """
    Args:
        team (str): _description_
    """

    logger = get_run_logger()
    logger.info("Hello World")


if __name__ == "__main__":
    run(wg_seatgeek, "Boston-Celtics")
