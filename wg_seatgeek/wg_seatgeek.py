"""
Prefect flow for use with seatgeek-client
"""
# from anyio import run
from prefect import flow, get_run_logger
from prefect.blocks.system import Secret


@flow
async def wg_seatgeek(team: str) -> None:
    """
    Args:
        team (str): _description_
    """

    logger = get_run_logger()
    logger.info("Hello World Test 2")


if __name__ == "__main__":
    artifact_reg_url: Secret = Secret.load("artifact-reg-url")
    # do nothing
