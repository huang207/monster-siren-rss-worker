# import aiohttp
from workers import fetch, handler
import json


@handler
async def get_handler(url):
    return await fetch(url)


urls = {
    "albums": "https://monster-siren.hypergryph.com/api/albums",
    "albumData": "https://monster-siren.hypergryph.com/api/album/{}/data",
    "albumDetail": "https://monster-siren.hypergryph.com/api/album/{}/detail",
    "songs": "https://monster-siren.hypergryph.com/api/songs",
    "song": "https://monster-siren.hypergryph.com/api/song/{}",
}


async def get_album(album_id):
    """
    Get the album details from the API.
    """
    album_url = urls["albumDetail"].format(album_id)

    # Get the datas of the album
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(urls["albumData"].format(album_id)) as response:
    #         if response.status != 200:
    #             raise Exception(f"Failed to fetch album details: {response.status}")
    #         json_data = await response.json()
    #         album_datas = json_data["data"]

    response = await get_handler(urls["albumData"].format(album_id))
    if response.status != 200:
        raise Exception(f"Failed to fetch album details: {response.status}")
    json_data = await response.json()
    album_datas = json_data["data"]

    if "code" not in json_data or json_data["code"] != 0:
        raise Exception(f"Failed to fetch album datas: {album_id}")

    # Get the details of the album
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(album_url) as response:
    #         if response.status != 200:
    #             raise Exception(f"Failed to fetch album details: {response.status}")
    #         json_data = await response.json()
    #         album_details = json_data["data"]

    response = await get_handler(album_url)
    if response.status != 200:
        raise Exception(f"Failed to fetch album details: {response.status}")
    json_data = await response.json()
    album_details = json_data["data"]

    if "code" not in json_data or json_data["code"] != 0:
        raise Exception(f"Failed to fetch album details: {album_id}")

    album_name = album_details["name"]
    album_cover = album_details["coverUrl"]
    ablum_artistes = ", ".join(album_datas["artistes"])

    # Store the album data in the dictionary
    album_data = {
        "album_id": album_id,
        "name": album_name,
        "artistes": ablum_artistes,
        "intro": album_details["intro"],
        "belong": album_details["belong"],
        "cover": album_cover,
        "songs": [],
    }

    # Iterate through each song in the album and get its details
    for song in album_details["songs"]:
        song_id = song["cid"]
        song_name = song["name"]
        song_artistes = ", ".join(song["artistes"])
        song_url = urls["song"].format(song_id)

        # Get the details of the song
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(song_url) as response:
        #         if response.status != 200:
        #             raise Exception(f"Failed to fetch song details: {response.status}")
        #         json_data = await response.json()
        #         song_details = json_data["data"]

        response = await get_handler(song_url)
        if response.status != 200:
            raise Exception(f"Failed to fetch song details: {response.status}")
        json_data = await response.json()
        song_details = json_data["data"]

        if "code" not in json_data or json_data["code"] != 0:
            continue
        # Store the song data in the dictionary
        album_data["songs"].append(
            {
                "id": song_id,
                "name": song_name,
                "artistes": song_artistes,
                "url": song_details["sourceUrl"],
                "lyric": song_details["lyricUrl"],
            }
        )

    return album_data
