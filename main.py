import os
import time
import sys
import random

from logging import getLogger, StreamHandler, INFO

from requests.structures import CaseInsensitiveDict
from requests.exceptions import RequestException

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

import lineworks as lw
import lineworks_sticker
import chatgpt

global_data = {}
RETRY_COUNT_MAX = 5
SCOPE = "bot"

# Settings for LINEWORKS
domain_id = os.environ.get("LW_DOMAIN_ID", "dummy")
deploy_env = os.environ.get("LW_API_BOT_ENV", "dummy")

if deploy_env == "prod":
    bot_id = os.environ.get("LW_API_BOT_ID_PROD", "dummy")
    bot_secret = os.environ.get("LW_API_BOT_SECRET_PROD", "dummy")
elif deploy_env == "dev":
    bot_id = os.environ.get("LW_API_BOT_ID_DEV", "dummy")
    bot_secret = os.environ.get("LW_API_BOT_SECRET_DEV", "dummy")

client_id = os.environ.get("LW_API_CLIENT_ID", "dummy")
client_secret = os.environ.get("LW_API_CLIENT_SECRET", "dummy")
service_account_id = os.environ.get("LW_API_SERVICE_ACCOUNT", "dummy")
privatekey = os.environ.get("LW_API_PRIVATEKEY", "dummy")

logger = getLogger(__name__)
handler = StreamHandler(sys.stdout)
handler.setLevel(INFO)
logger.addHandler(handler)
logger.setLevel(INFO)

# FastAPI
app = FastAPI()

app.mount("/woff", StaticFiles(directory="static/woff", html=True), name="woff")


def __send_message(is_talk_room: bool, res_text: str, to_channel_id: str, to_user_id: str):
    # send message
    for i in range(RETRY_COUNT_MAX):
        try:
            # Reply message
            if is_talk_room:
                res = lw.send_message_to_channel(res_text,
                                                 bot_id,
                                                 to_channel_id,
                                                 to_user_id,
                                                 global_data["access_token"])
            else:
                res = lw.send_message_to_user(res_text,
                                              bot_id,
                                              to_user_id,
                                              global_data["access_token"])
        except RequestException as e:
            body = e.response.json()
            status_code = e.response.status_code
            if status_code == 403:
                if body["code"] == "UNAUTHORIZED":
                    # Access Token has been expired.
                    # Update Access Token
                    logger.info("Update access token")
                    res = lw.get_access_token(client_id,
                                              client_secret,
                                              service_account_id,
                                              privatekey,
                                              SCOPE)
                    global_data["access_token"] = res["access_token"]
                else:
                    logger.exception(e)
                    break
            elif status_code == 429:
                # Requests over rate limit.
                logger.info("Over rate limit")
                logger.info(body)
            else:
                logger.exception(e)
                break

            # wait and retry
            time.sleep(2 ** i)
        else:
            break


def __send_sticker(is_talk_room: bool, package_id: str, sticker_id: str, to_channel_id: str, to_user_id: str):
    # send sticker
    for i in range(RETRY_COUNT_MAX):
        try:
            # Reply message
            if is_talk_room:
                res = lw.send_sticker_to_channke(package_id,
                                                 sticker_id,
                                                 bot_id,
                                                 to_channel_id,
                                                 to_user_id,
                                                 global_data["access_token"])
            else:
                res = lw.send_sticker_to_user(package_id,
                                              sticker_id,
                                              bot_id,
                                              to_user_id,
                                              global_data["access_token"])
        except RequestException as e:
            body = e.response.json()
            status_code = e.response.status_code
            if status_code == 403:
                if body["code"] == "UNAUTHORIZED":
                    # Access Token has been expired.
                    # Update Access Token
                    logger.info("Update access token")
                    res = lw.get_access_token(client_id,
                                              client_secret,
                                              service_account_id,
                                              privatekey,
                                              SCOPE)
                    global_data["access_token"] = res["access_token"]
                else:
                    logger.exception(e)
                    break
            elif status_code == 429:
                # Requests over rate limit.
                logger.info("Over rate limit")
                logger.info(body)
            else:
                logger.exception(e)
                break

            # wait and retry
            time.sleep(2 ** i)
        else:
            break


@app.post("/callback")
async def callback(request: Request):
    body_raw = await request.body()
    body_json = await request.json()
    headers = CaseInsensitiveDict(request.headers)
    header_bot_id = headers.get("x-works-botid", "dummy")
    signature = headers.get("x-works-signature", "dummy")

    logger.debug("Headers: {}".format(headers))
    logger.debug("Body: {}".format(body_json))

    # Validation
    signature = headers.get("x-works-signature")
    if header_bot_id != bot_id or not lw.validate_request(body_raw, signature, bot_secret):
        logger.warn("Invalid request")
        return

    # Receive message
    if "channelId" in body_json["source"]:
        from_channel_id = body_json["source"]["channelId"]
        to_channel_id = from_channel_id
        is_talk_room = True
    else:
        is_talk_room = False

    from_user_id = body_json["source"]["userId"]
    to_user_id = from_user_id

    content = body_json["content"]
    content_type = body_json["content"]["type"]

    # Generate response
    if content_type == "text":
        content_text = content["text"]
    elif content_type == "location":
        content_text = content["address"]
    elif content_type == "sticker":
        content_text = "スタンプ送ります"
    elif content_type == "image":
        content_text = "画像送ります"
    elif content_type == "file":
        content_text = "ファイル送ります"
    else:
        content_text = "こんにちは"

    res_text = chatgpt.generate_response(content_text)

    # lineworks reply process
    if "access_token" not in global_data:
        # Get Access Token
        logger.info("Get access token")
        res = lw.get_access_token(client_id,
                                  client_secret,
                                  service_account_id,
                                  privatekey,
                                  SCOPE)
        global_data["access_token"] = res["access_token"]

    __send_message(is_talk_room, res_text, to_channel_id, to_user_id)

    # choose sticker
    sticker_id, package_id = random.choice(lineworks_sticker.stickers)

    __send_sticker(is_talk_room, package_id, sticker_id,
                   to_channel_id, to_user_id)

    return {}
