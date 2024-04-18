"""
Prefect flow for use with seatgeek-client
"""
# from anyio import run
from prefect import flow, get_run_logger
from prefect.blocks.system import Secret
from prefect.deployments import DeploymentImage


@flow
async def wg_seatgeek(team: str) -> None:
    """
    Args:
        team (str): _description_
    """

    logger = get_run_logger()
    logger.info("Hello World")


if __name__ == "__main__":
    artifact_reg_url: Secret = Secret.load("artifact-reg-url")

    wg_seatgeek.deploy(
        name="my-code-baked-into-an-image-deployment",
        work_pool_name="central-push-pool",
        image=DeploymentImage(
            name="us-central1-docker.pkg.dev/wade-prefect/prefect-images/prefect-flows/wg-seatgeek",  # noqa
            tag="test-tag",
            dockerfile="Dockerfile",
            platform="linux/amd64",
            buildargs={"AUTHED_ARTIFACT_REG_URL": artifact_reg_url.get()},
        ),
    )
