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
import whisper
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


@app.route("/webbrowsing", methods=["GET", "POST"])
def web_browsing():
    query = request.get_json(force=True)["query"]
    history = request.get_json(force=True)["history"]
    max_tokens = request.get_json(force=True)["max_tokens"]
    model = request.get_json(force=True)["model"]
    user = request.get_json(force=True)["user"]

    # gpt-3.5 model for default
    default_gpt35_model = AzureChatOpenAI(
        openai_api_base="https://chatbotapi1.openai.azure.com",
        openai_api_version="2023-03-15-preview",
        deployment_name="chatgptapi",
        openai_api_key="cfd349e9242e4495bad6aa347a16b0c9",
        openai_api_type="azure",
    )

    # gpt-4-8k model for default
    default_gpt4_8k_model = AzureChatOpenAI(
        openai_api_base="https://chatbotapi1.openai.azure.com",
        openai_api_version="2023-03-15-preview",
        deployment_name="chatgpt4api",
        openai_api_key="cfd349e9242e4495bad6aa347a16b0c9",
        openai_api_type="azure",
    )

    # gpt-4-32k model for default
    default_gpt4_32k_model = AzureChatOpenAI(
        openai_api_base="https://chatbotapi1.openai.azure.com",
        openai_api_version="2023-03-15-preview",
        deployment_name="chatgpt4_32_api",
        openai_api_key="cfd349e9242e4495bad6aa347a16b0c9",
        openai_api_type="azure",
    )

    # gpt-3.5 model for /9
    nine_gpt35_model = AzureChatOpenAI(
        openai_api_base="https://openai-99.openai.azure.com",
        openai_api_version="2023-03-15-preview",
        deployment_name="gpt3-5",
        openai_api_key="921a52075c0749d68f1ad15d1bee0a05",
        openai_api_type="azure",
    )

    # gpt-4-8k model for /9
    nine_gpt4_8k_model = AzureChatOpenAI(
        openai_api_base="https://openai-99.openai.azure.com",
        openai_api_version="2023-03-15-preview",
        deployment_name="gpt4-8k",
        openai_api_key="921a52075c0749d68f1ad15d1bee0a05",
        openai_api_type="azure",
    )

    # gpt-4-32k model for /9
    nine_gpt4_32k_model = AzureChatOpenAI(
        openai_api_base="https://openai-99.openai.azure.com",
        openai_api_version="2023-03-15-preview",
        deployment_name="gpt4-32k",
        openai_api_key="921a52075c0749d68f1ad15d1bee0a05",
        openai_api_type="azure",
    )

    # set api key, api base and deployment based on user
    if user == "9":
        if model == "gpt-35":
            llm_model = nine_gpt35_model
        elif model == "gpt-4-8k":
            llm_model = nine_gpt4_8k_model
        elif model == "gpt-4-32k":
            llm_model = nine_gpt4_32k_model
    else:
        if model == "gpt-35":
            llm_model = default_gpt35_model
        elif model == "gpt-4-8k":
            llm_model = default_gpt4_8k_model
        elif model == "gpt-4-32k":
            llm_model = default_gpt4_32k_model

    # set up tools to be used
    tools = load_tools(
        [
            "llm-math",  # calculator
            "pal-math",  # solve complex word math problems
            "wikipedia",  # wiki
        ],
        llm=llm_model,
    )

    # get google search links
    def get_google_search_links(question: str) -> list:
        """Used to get the top 3 most relevant URLs from Google search based off a query."""
        links = []
        for url in search(question, tld="com", num=10, stop=10, pause=2):
            links.append(url)
        return links[0:3]

    # create structured tool for get_text_from_url
    google_search_link = StructuredTool.from_function(get_google_search_links)

    # append to tools
    tools.append(google_search_link)

    # retrieve plaintext only from a given URL
    def get_text_from_url(url: str) -> str:
        """Used for extracting text only from a given URL without the HTMl element tags.
        Can be chained with google_search_link to get information for each URL."""
        service = Service(executable_path=r"./chromedriver")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        scraped_text = driver.find_element("xpath", "/html/body").text
        driver.quit()
        return scraped_text

    # create structured tool for get_text_from_url
    text_from_url = StructuredTool.from_function(get_text_from_url)

    # append to tools
    tools.append(text_from_url)

    # create new ChatMessageHistory
    message_history = ChatMessageHistory()

    i = 0

    # add message history retrieved from frontend to the created ChatMessgeHistory
    while i < len(history):
        if history[i]["role"] == "user":  # human message
            message_history.add_user_message(history[i]["content"])
        else:  # assistant/ai message
            message_history.add_ai_message(history[i]["content"])
        i = i + 1

    # keep memory of convo chain
    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=message_history, return_messages=True
    )

    # initialize conversational agent with tools
    agent_chain = initialize_agent(
        tools,
        llm_model,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )

    # run the query
    result = agent_chain.run(query)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
