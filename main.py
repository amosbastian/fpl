from fpl import FPL
import aiohttp
import asyncio
import os
import configparser

async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)

        config = configparser.ConfigParser()
        config.read('credentials.cfg')
        os.environ['FPL_EMAIL'] = config['CREDS']['FPL_EMAIL']
        os.environ['FPL_PASSWORD'] = config['CREDS']['FPL_PASSWORD']

        await fpl.login()
        h2h_league = await fpl.get_h2h_league(829116)
    print(h2h_league)

# Python 3.7+
asyncio.run(main())