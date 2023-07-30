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



    # send request to api
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        api_key="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",
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

   
   


    # send request to api
    response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
        api_key="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",
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
    

    

    # send request to api
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        api_key="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",
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
    user_query = request.get_json(force=True)["url"]

    print(f"####### whisperapi ##### userquery: {user_query} ")

    # get vid content
    youtube_vid_content = YouTube(user_query)

    # get audio only
    audio_streams = youtube_vid_content.streams.filter(only_audio=True)

    # 0: 48kbps, 1: 128kbps, 2: 160kbps
    audio_stream = audio_streams[2]

    audio_file_path = "temp.mp3"

    # download audio file
    audio_stream.download(filename=audio_file_path)

    audio_file = open(audio_file_path, "rb")

    # transcribe audio
    result = openai.Audio.transcribe(
        api_key=("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"),
        model="whisper-1",
        file=audio_file,
    )

    print("Transcription:\n", result["text"])

    # set messages for GPT API call
    system_msg = (
        "You are a helpful assistant who is great at summarizing large amounts of text."
    )
    user_msg = "Summarize the following text: " + result["text"]

    # summarize the transcription
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        api_key="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",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,
    )

    audio_file.close()

    # delete audio file
    os.remove(audio_file_path)

    # get response and return in json format
    reply = response["choices"][0]["message"]["content"]
    returner = {"Summary": reply}
    print(returner)
    return jsonify(returner)


if __name__ == "__main__":
    app.run(debug=True)
