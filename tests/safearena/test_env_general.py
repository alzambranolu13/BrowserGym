import gymnasium as gym
import logging
import os
import playwright.sync_api
import pytest
import random

from tenacity import retry, stop_after_attempt, retry_if_exception_type

# register gym environments
import browsergym.safearena


__SLOW_MO = 1000 if "DISPLAY_BROWSER" in os.environ else None
__HEADLESS = False if "DISPLAY_BROWSER" in os.environ else True


from browsergym.safearena import ALL_SAFEARENA_TASK_IDS

rng = random.Random(1)
task_ids = rng.sample(ALL_SAFEARENA_TASK_IDS, 25)


@retry(
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(playwright.sync_api.TimeoutError),
    reraise=True,
    before_sleep=lambda _: logging.info("Retrying due to a TimeoutError..."),
)
@pytest.mark.parametrize("task_id", task_ids)
@pytest.mark.slow
def test_env_generic(task_id):
    env = gym.make(
        f"browsergym/{task_id}",
        headless=__HEADLESS,
        slow_mo=__SLOW_MO,
    )
    obs, info = env.reset()

    env.close()


