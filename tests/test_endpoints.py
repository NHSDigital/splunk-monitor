from os import getenv

import pytest
import requests


@pytest.mark.e2e
@pytest.mark.smoketest
@pytest.mark.asyncio
async def test_wait_for_ping(nhsd_apim_proxy_url):
    """
        test for _ping, this waits until the correct SOURCE_COMMIT_ID ( from env var )
        is available
    """
    retries = 0
    resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
    deployed_commit_id = resp.json().get("commitId")

    while (deployed_commit_id != getenv('SOURCE_COMMIT_ID')
            and retries <= 30
            and resp.status_code == 200):
        resp = requests.get(f"{nhsd_apim_proxy_url}/_ping")
        deployed_commit_id = resp.json().get("commitId")
        retries += 1

    if resp.status_code != 200:
        pytest.fail(f"Status code {resp.status_code}, expecting 200")
    elif retries >= 30:
        pytest.fail("Timeout Error - max retries")

    assert deployed_commit_id == getenv('SOURCE_COMMIT_ID')
