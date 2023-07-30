# main python file to be running on VM

from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chat_models import AzureChatOpenAI
from langchain.tools import StructuredTool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory import ChatMessageHistory

from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube
from googlesearch import search
import openai

# import whisper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import os

app = Flask(__name__)

CORS(app)


@app.route("/summarize", methods=["GET", "POST"])  # webpage summary
def summarize_webpage():
    user = request.get_json(force=True)["user"]
    model = request.get_json(force=True)["model"]

    # get text only using Selenium to scrape web text content
    url = request.get_json(force=True)["url"]
    service = Service(executable_path=r"./chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    scraped_text = driver.find_element("xpath", "/html/body").text
    driver.quit()

    # set api key, api base and deployment based on user
    if user == "9":
        openai.api_key = "921a52075c0749d68f1ad15d1bee0a05"
        openai.api_base = "https://openai-99.openai.azure.com"
        if model == "gpt-35":
            deployment = "gpt3-5"
        elif model == "gpt-4-8k":
            deployment = "gpt4-8k"
        elif model == "gpt-4-32k":
            deployment = "gpt4-32k"
    else:
        openai.api_key = "cfd349e9242e4495bad6aa347a16b0c9"
        openai.api_base = "https://chatbotapi1.openai.azure.com"
        if model == "gpt-35":
            deployment = "chatgptapi"
        elif model == "gpt-4-8k":
            deployment = "chatgpt4api"
        elif model == "gpt-4-32k":
            deployment = "chatgpt4_32_api"

    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"

    # send request to api
    response = openai.ChatCompletion.create(
        engine=deployment,  # gpt3.5 deployment
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who is great at summarizing large amounts of text.",
            },
            {"role": "user", "content": "Summarize this: " + scraped_text},
        ],
    )

    returner = "SUMMARY:\n" + response["choices"][0]["message"]["content"]

    return jsonify(returner)


# webpage keyword extraction
@app.route("/keyword", methods=["GET", "POST"])
def extract_webpage():
    user = request.get_json(force=True)["user"]
    model = request.get_json(force=True)["model"]

    # get text only
    url = request.get_json(force=True)["url"]
    service = Service(executable_path=r"./chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    scraped_text = driver.find_element("xpath", "/html/body").text
    driver.quit()

    # set api key, api base and deployment based on user
    if user == "9":
        openai.api_key = "921a52075c0749d68f1ad15d1bee0a05"
        openai.api_base = "https://openai-99.openai.azure.com"
        if model == "gpt-35":
            deployment = "gpt3-5"
        elif model == "gpt-4-8k":
            deployment = "gpt4-8k"
        elif model == "gpt-4-32k":
            deployment = "gpt4-32k"
    else:
        openai.api_key = "cfd349e9242e4495bad6aa347a16b0c9"
        openai.api_base = "https://chatbotapi1.openai.azure.com"
        if model == "gpt-35":
            deployment = "chatgptapi"
        elif model == "gpt-4-8k":
            deployment = "chatgpt4api"
        elif model == "gpt-4-32k":
            deployment = "chatgpt4_32_api"

    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"

    # send request to api
    response = openai.ChatCompletion.create(
        engine=deployment,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who is great at extracting keywords from text.",
            },
            {"role": "user", "content": "Extract keywords from this: " + scraped_text},
        ],
    )

    returner = "EXTRACTED KEYWORDS:\n" + response["choices"][0]["message"]["content"]

    return jsonify(returner)


# webpage translation
@app.route("/translate", methods=["GET", "POST"])
def translate_webpage():
    user = request.get_json(force=True)["user"]
    model = request.get_json(force=True)["model"]

    # get text only
    url = request.get_json(force=True)["url"]
    language = request.get_json(force=True)["language"]
    service = Service(executable_path=r"./chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    scraped_text = driver.find_element("xpath", "/html/body").text
    driver.quit()

    # set api key, api base and deployment based on user
    if user == "9":
        openai.api_key = "921a52075c0749d68f1ad15d1bee0a05"
        openai.api_base = "https://openai-99.openai.azure.com"
        if model == "gpt-35":
            deployment = "gpt3-5"
        elif model == "gpt-4-8k":
            deployment = "gpt4-8k"
        elif model == "gpt-4-32k":
            deployment = "gpt4-32k"
    else:
        openai.api_key = "cfd349e9242e4495bad6aa347a16b0c9"
        openai.api_base = "https://chatbotapi1.openai.azure.com"
        if model == "gpt-35":
            deployment = "chatgptapi"
        elif model == "gpt-4-8k":
            deployment = "chatgpt4api"
        elif model == "gpt-4-32k":
            deployment = "chatgpt4_32_api"

    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"

    # send request to api
    response = openai.ChatCompletion.create(
        engine=deployment,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who is great at translating text. Do not summarize the text. Translate the main content of the text only.",
            },
            {
                "role": "user",
                "content": "Translate this to " + language + " : " + scraped_text,
            },
        ],
    )

    returner = "TRANSLATION:\n" + response["choices"][0]["message"]["content"]

    return jsonify(returner)


# yt transcription and summary
@app.route("/youtube", methods=["GET", "POST"])
def youtube_transcription():
    url = request.get_json(force=True)["url"]
    user = request.get_json(force=True)["user"]
    model = request.get_json(force=True)["model"]

    # set api key, api base and deployment based on user, using GPT4-8K model
    if user == "9":
        openai.api_key = "921a52075c0749d68f1ad15d1bee0a05"
        openai.api_base = "https://openai-99.openai.azure.com"
        deployment = "gpt4-8k"
    else:
        openai.api_key = "cfd349e9242e4495bad6aa347a16b0c9"
        openai.api_base = "https://chatbotapi1.openai.azure.com"
        deployment = "chatgpt4api"

    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"

    # get vid content
    youtube_vid_content = YouTube(url)

    # get audio only
    audio_streams = youtube_vid_content.streams.filter(only_audio=True)

    # 0: 48kbps, 1: 128kbps, 2: 160kbps
    audio_stream = audio_streams[2]

    # download audio file
    audio_stream.download(filename="temp.mp3")

    # transcribe audio and get transcription
    model = whisper.load_model(model)
    result = model.transcribe("temp.mp3", fp16=False)
    transcription = result["text"]

    # summarize the transcription
    response = openai.ChatCompletion.create(
        engine=deployment,  # gpt4-8k deployment
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who is great at summarizing large amounts of text.",
            },
            {
                "role": "user",
                "content": "Summarize the following text: " + transcription,
            },
        ],
    )
    summary = response["choices"][0]["message"]["content"]

    # delete audio file
    os.remove("temp.mp3")

    # get translation to English
    response = openai.ChatCompletion.create(
        engine=deployment,  # gpt4-8k deployment
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who is great at translating large amounts of text.",
            },
            {
                "role": "user",
                "content": "Translate the following text to English: " + transcription,
            },
        ],
    )
    eng_translation = response["choices"][0]["message"]["content"]

    # get summary in English
    response = openai.ChatCompletion.create(
        engine=deployment,  # gpt4-8k deployment
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who is great at summarizing large amounts of text.",
            },
            {
                "role": "user",
                "content": "Summarize the following text: " + eng_translation,
            },
        ],
    )
    eng_summary = response["choices"][0]["message"]["content"]

    # return content required
    returner = (
        "TRANSCRIPTION:\n"
        + transcription
        + "\n\nSUMMARY:\n"
        + summary
        + "\n\nENGLISH TRANSLATION:\n"
        + eng_translation
        + "\n\nENGLISH SUMMARY:\n"
        + eng_summary
    )
    return jsonify(returner)


if __name__ == "__main__":
    app.run(debug=True)
