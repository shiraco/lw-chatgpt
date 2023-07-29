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
bot_id = os.environ.get("LW_API_BOT_ID", "dummy")
bot_secret = os.environ.get("LW_API_BOT_SECRET", "dummy")
client_id = os.environ.get("LW_API_CLIENT_ID", "dummy")
client_secret = os.environ.get("LW_API_CLIENT_SECRET", "dummy")
service_account_id = os.environ.get("LW_API_SERVICE_ACCOUNT", "dummy")
privatekey = os.environ.get("LW_API_PRIVATEKEY", "dummy")

logger = getLogger(__name__)
handler = StreamHandler(sys.stdout)
handler.setLevel(INFO)
logger.addHandler(handler)
logger.setLevel(INFO)

app = FastAPI()

app.mount("/woff", StaticFiles(directory="static/woff", html=True), name="woff")

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
    from_user_id = body_json["source"]["userId"]
    content = body_json["content"]

    # Generate response
    res_text = chatgpt.generate_response(content["text"])
    to_user_id = from_user_id

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

    # send message
    for i in range(RETRY_COUNT_MAX):
        try:
            # Reply message
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

    # choose sticker
    sticker_id, package_id = random.choice(lineworks_sticker.stickers)

    # send sticker
    for i in range(RETRY_COUNT_MAX):
        try:
            # Reply message
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


    return {}
