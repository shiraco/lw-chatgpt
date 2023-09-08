import os

import openai

from dotenv import load_dotenv
load_dotenv()

# Settings for OpenAI
openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_response(text: str) -> str:
    """Generate response from ChatGPT

    :param text: request text
    :return: generated text
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "関西弁で話して"},
            {"role": "system", "content": "発言の最後に「知らんけど。」をつけて"},
            {"role": "user", "content": text},
        ],
    )
    res = response.choices[0]["message"]["content"].strip()

    return res

def generate_response(*contents) -> str:
    """Generate response from ChatGPT

    :param text: request text
    :return: generated text
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=contents,
    )
    res = response.choices[0]["message"]["content"].strip()

    return res
