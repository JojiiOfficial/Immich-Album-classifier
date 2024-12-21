import json
from typing import Optional

import requests

from config import INSTANCE, TOKEN, CLIENT_CERT, CLIENT_KEY

CERT = (CLIENT_CERT, CLIENT_KEY)


def get_all_assets(payload: dict = {}):
    path = "/api/search/metadata"
    next_page = None

    assets = []

    while True:
        if next_page is not None:
            payload['page'] = next_page
        res = do_immich_request(INSTANCE, path, token=TOKEN, cert=CERT, payload=payload)['assets']
        assets.extend(res['items'])
        if "nextPage" in res and res['nextPage'] is not None:
            next_page = res['nextPage']
        else:
            break

    return assets


def create_album(name: str, add_assets: Optional[list[str]]):
    path = "/api/albums"
    payload = {
        "albumName": name,
        "assetIds": add_assets,
    }
    return do_immich_request(INSTANCE, path, token=TOKEN, method="POST", cert=CERT, payload=payload)


def get_all_albums():
    path = "/api/albums"
    return do_immich_request(INSTANCE, path, TOKEN, method="GET", cert=CERT)


def delete_album(album_id: str):
    path = f"/api/albums/{album_id}"
    do_immich_request(INSTANCE, path, TOKEN, method="DELETE", cert=CERT, raw=True, do_json=False).raise_for_status()


def add_assets_to_album(asset_ids: list[str], album_id: str):
    path = f"/api/albums/{album_id}/assets"
    payload = {
        "ids": asset_ids
    }
    do_immich_request(INSTANCE, path, TOKEN, payload, method="PUT", cert=CERT)


def download_asset(asset_id: str, output_file: str):
    path = f"/api/assets/{asset_id}/original"
    response = do_immich_request(INSTANCE, path, token=TOKEN, cert=CERT, method="GET", do_json=False, raw=True,
                                 stream=True)
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)


def do_immich_request(instance: str, path: str, token: str, payload: dict = {}, method: str = "POST",
                      cert: Optional[tuple[str, str]] = None, do_json: bool = True, stream: bool = False,
                      raw: bool = False):
    url = instance + path

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': token
    }

    if stream and raw:
        headers["Accept"] = 'application/octet-stream'
    else:
        headers["Accept"] = "application/json"

    if cert is not None:
        if not cert[0].strip() and not cert[1].strip():
            cert = None

    response = requests.request(method, url, headers=headers, data=json.dumps(payload), cert=cert, stream=stream)
    if do_json:
        return response.json()
    else:
        if raw:
            return response
        else:
            return response.text
