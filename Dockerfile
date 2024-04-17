FROM prefecthq/prefect:2.17-python3.11
ARG AUTHED_ARTIFACT_REG_URL
COPY requirements.txt .
RUN python -m pip install --extra-index-url ${AUTHED_ARTIFACT_REG_URL} -r requirements.txt
RUN apt-get update
