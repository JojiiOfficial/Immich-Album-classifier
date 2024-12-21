import ollama
from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm

import immich
import utils
from config import TAG_PREFIX, SCALE, ALL_TAGS, MODEL

register_heif_opener()

MAX_FAILS = 40  # Max failures in a row until we abort.

all_assets = immich.get_all_assets()

# Load potentially existing albums
existing_albums = dict()
for album in immich.get_all_albums():
    if not album['albumName'].startswith(TAG_PREFIX):
        continue
    existing_albums[album['albumName'][len(TAG_PREFIX):]] = album['id']

# Check and prompt for deletion of existing classifications
if len(existing_albums) > 0 and len(TAG_PREFIX.strip()) > 0:
    to_delete_albums = ", ".join([f"{TAG_PREFIX}{x}" for x in existing_albums.keys()])
    if utils.confirmation_prompt(f"Delete existing AI generated albums: ({to_delete_albums})"):
        for album in immich.get_all_albums():
            if album['albumName'].startswith(TAG_PREFIX):
                immich.delete_album(album['id'])

        existing_albums.clear()

fail_counter = 0

for asset in tqdm(all_assets):
    asset_id = asset['id']

    mime = asset['originalMimeType']
    if not mime.lower().startswith("image"):
        print(f"Skipping mime type: {mime}")
        continue

    try:
        immich.download_asset(asset_id, "./img.png")

        image = Image.open("./img.png")
        image.thumbnail((image.width * SCALE, image.height * SCALE))
        image.save("./th.png")

        response = ollama.chat(
            model=MODEL,
            messages=[{
                'role': 'user',
                'content': 'Classify the given image into one of the given categories.' +
                           'Only respond with the exact category tag.' +
                           'You must never respond with a non existing token!' +
                           'Do not respond with a description or anything else than the category' +
                           'Use only the exact category name and only ONE!' +
                           'Pick ONE of the following categories: ' + ", ".join([f"\"{x}\"" for x in ALL_TAGS]),
                'images': ['./th.png']
            }],
            options={"temperature": 0.1}
        )

        # Strip tailing punctuation.
        tag = response.message.content.strip()
        if tag.endswith('.'):
            tag = tag[:len(tag) - 1]

        # print(tag)

        # Assign picture to album and create if necessary.
        if tag not in existing_albums:
            album_id = immich.create_album(f"{TAG_PREFIX}{tag}", add_assets=[asset_id])['id']
            existing_albums[tag] = album_id
        else:
            album_id = existing_albums[tag]
            immich.add_assets_to_album([asset_id], album_id)

        fail_counter = 0

    except Exception as e:
        print("Skipping", asset['originalFileName'], f"exception: {e}")

        if fail_counter > MAX_FAILS:
            print(f"Too many failures (>{MAX_FAILS}). Exiting!")
            exit(1)

        fail_counter += 1
