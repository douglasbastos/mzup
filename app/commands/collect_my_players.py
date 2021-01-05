import asyncio
import json

import requests
from aiohttp import ClientSession

from app.config import MZ_URL_LIST_PLAYERS, MZ_URL_SCOUT_REPORT, MZ_URL_TRAINING_HISTORY
from app.driver import chrome
from app.services import reqasync
from app.services.login import get_session_id, login
from app.services.players import Players


def request_players(browser):
    response = requests.get(MZ_URL_LIST_PLAYERS, cookies={'PHPSESSID': get_session_id(browser)})
    result = json.loads(response.content.decode())

    return result


async def get_info_players(player_ids: list, part_url: str, session_mz_id: str):
    cookies = {'PHPSESSID': session_mz_id}
    async with ClientSession(cookies=cookies) as session:
        tasks = []
        player_ids = list(player_ids)
        for player_id in player_ids:
            url = part_url.format(player_id)
            sema = asyncio.Semaphore(30)
            tasks.append(reqasync.get(url, session=session, sema=sema))

        return await asyncio.gather(*tasks)


async def main():
    with chrome() as browser:
        login(browser)
        result = request_players(browser)

        players = Players(result['players'])
        info_players = dict(players.get())
        player_ids = result['player_ids']

        call_to_collect_extra_info = {
            (MZ_URL_SCOUT_REPORT, players.scout_report, 'scout_report'),
            (MZ_URL_TRAINING_HISTORY, players.maximizations, 'maximizations')
        }

        for part_url, call, fieldname in call_to_collect_extra_info:
            player_scout_reports = await get_info_players(
                player_ids, part_url, get_session_id(browser)
            )

            for player_id, response in zip(player_ids, player_scout_reports):
                if body := response.decode():
                    info_players[player_id].update({fieldname: call(body)})
