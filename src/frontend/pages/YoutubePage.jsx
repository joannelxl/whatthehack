import React, { useState } from "react";
import Select from "react-select";
import { Tooltip } from "react-tooltip";
import axios from "axios";
import Moment from "moment";

import "./YoutubePage.css";

import { ThreeDots } from "react-loader-spinner";
import HelpOutlineOutlinedIcon from "@mui/icons-material/HelpOutlineOutlined";

function YoutubePage() {
  const [tooltipEnabled, setTooltipEnabled] = useState(false);

  const [url, setUrl] = useState(null);
  const [response, setResponse] = useState(null);
  const [completedStatus, setCompletedStatus] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState(false);

  const [user, setUser] = useState(
    window.location.pathname.split("/").pop() === "9" ? "9" : "default"
  );

  // default model is base
  const [selectedModel, setSelectedModel] = useState({
    value: "base",
    label: "base",
  });

  // Whisper models
  const models = [
    { value: "tiny", label: "tiny" },
    { value: "base", label: "base" },
    { value: "small", label: "small" },
    { value: "medium", label: "medium" },
    { value: "large-v2", label: "large" },
  ];

  // upon submission of url
  function handleRun(e) {
    e.preventDefault();
    submitQuery(
      "https://dxclnvmonline2.eastus.cloudapp.azure.com:8080/youtube",
      {
        url: url,
        user: user,
        model: selectedModel.value,
        headers: {
          "Access-Control-Allow-Headers": "Content-Type",
          "Content-Type": "application/json",
          "Access-Control-Allow-Credentials": "true",
          "Access-Control-Allow-Origin":
            "https://polite-mud-0e3eb4d10.2.azurestaticapps.net",
          "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        },
      }
    );
    setLoadingStatus(true);
  }

  // set url when user input in input box changes
  async function handleChange(e) {
    await setUrl(e.target.value);
  }

  // download file upon button click
  function handleDownload(e) {
    exportFile(response);
  }

  // clear text input and set completed status to false
  function handleClear(e) {
    let urlInput = document.getElementById("url-input");
    urlInput.value = null;
    setUrl(null);
    setCompletedStatus(false);
    setLoadingStatus(false);
  }

  //function to write to file
  function exportFile(fileContent) {
    if (fileContent.at(0) === '"' && fileContent.at(-1) === '"') {
      fileContent = fileContent.slice(1, -1);
    }
    const element = document.createElement("a");
    const file = new Blob([fileContent], { type: "text/plain" });
    element.href = window.URL.createObjectURL(file);
    element.download = "url_yt_" + Moment().format("MMDDhhmmss") + ".txt";
    document.body.appendChild(element);
    element.click();
  }

  // send request to API through axios
  function submitQuery(path, queryObj) {
    axios.post(path, queryObj).then(
      (reply) => {
        setResponse(reply.data);
        setLoadingStatus(false);
        setCompletedStatus(true);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  return (
    <>
      <div class="youtubepage-content">
        <div class="youtube-top-bar">
          <div class="btn-group">
            <button
              type="button"
              onClick={() => {
                setTooltipEnabled(true);
              }}
            >
              <HelpOutlineOutlinedIcon class="btn-icon" />
              <span className="btn-text"> Show User Guide </span>
            </button>
          </div>
          <div class="select-whisper-btn">
            <span class="select-text"> Select transcription model: </span>
            <Select
              id="select-model"
              defaultValue={selectedModel}
              onChange={setSelectedModel}
              options={models}
              placeholder="Select Model"
            />
          </div>
        </div>
        <div class="youtube-main-content">
          <br></br>
          <br></br>
          <h2 className="text-2xl font-bold self-center">
            Transcribe and Summarize your YouTube video
          </h2>
          <br></br>
          <br></br>
          <h4 className="self-center">
            {" "}
            Video should only be around 10 minutes long (due to OpenAI's token
            limitation){" "}
          </h4>
          <br></br>
          <div id="enter-url"></div>
          <div className="flex flex-col">
            <div className="flex flex-row w-full items-center">
              <h4 className="text-base font-medium ml-4 mr-2 "> URL: </h4>
              <div className="relative w-full">
                <input
                  type="text"
                  id="url-input"
                  className="h-12 bg-[#F8F9FA] border border-black text-gray-900 text-base rounded-3xl block w-full pl-8 pr-12 py-1 outline-none cursor-text"
                  placeholder="Input your URL..."
                  onChange={handleChange}
                />
              </div>
              {completedStatus == false && loadingStatus == false && (
                <button
                  className="rounded-md bg-blue-500 text-[#FFFFFF] w-fit mx-2"
                  id="run-button"
                  onClick={handleRun}
                >
                  Run
                </button>
              )}
              {completedStatus == false && loadingStatus == true && (
                <button
                  className="rounded-md bg-blue-500 text-[#FFFFFF] w-fit mx-2"
                  id="run-button"
                  disabled={true}
                >
                  <ThreeDots
                    height="20"
                    width="20"
                    radius="9"
                    color="#4fa94d"
                    ariaLabel="three-dots-loading"
                    wrapperStyle={{}}
                    wrapperClassName=""
                    visible={true}
                  />
                </button>
              )}
              {completedStatus == true && (
                <button
                  className="rounded-md bg-gray-400 text-[#FFFFFF] w-fit mx-2"
                  id="run-button"
                  disabled={true}
                >
                  Run
                </button>
              )}
              <button
                className="rounded-md bg-red-500 text-[#FFFFFF] w-fit ml-2 mr-4"
                id="clear-button"
                onClick={handleClear}
              >
                Clear
              </button>
            </div>
            <br></br>
            <div className="flex flex-row justify-center w-full">
              {completedStatus == false && (
                <button
                  id="download-button"
                  className="rounded-md bg-gray-400 text-[#FFFFFF] w-fit mx-2"
                  disabled={true}
                >
                  Download output file
                </button>
              )}
              {completedStatus == true && (
                <button
                  id="download-button"
                  className="rounded-md bg-green-500 text-[#FFFFFF] w-fit mx-2"
                  onClick={handleDownload}
                >
                  Download output file
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
      <Tooltip
        anchorSelect="#enter-url"
        variant="info"
        isOpen={tooltipEnabled}
        clickable
      >
        Enter your Youtube URL here. Click Run to submit.
        <a> </a>
        <a
          className="font-bold underline"
          onClick={() => setTooltipEnabled(false)}
        >
          Close
        </a>
      </Tooltip>
      <Tooltip
        anchorSelect="#run-button"
        variant="info"
        isOpen={tooltipEnabled}
        clickable
      >
        Submit your URL.
        <a> </a>
        <a
          className="font-bold underline"
          onClick={() => setTooltipEnabled(false)}
        >
          Close
        </a>
      </Tooltip>
      <Tooltip
        anchorSelect="#clear-button"
        place="bottom"
        variant="info"
        isOpen={tooltipEnabled}
        clickable
      >
        Clear your URL.
        <a> </a>
        <a
          className="font-bold underline"
          onClick={() => setTooltipEnabled(false)}
        >
          Close
        </a>
      </Tooltip>
      <Tooltip
        anchorSelect="#download-button"
        place="bottom"
        variant="info"
        isOpen={tooltipEnabled}
        clickable
      >
        Download the output file when button turns green.
        <a> </a>
        <a
          className="font-bold underline"
          onClick={() => setTooltipEnabled(false)}
        >
          Close
        </a>
      </Tooltip>
      <Tooltip
        anchorSelect="#select-model"
        place="bottom"
        variant="info"
        isOpen={tooltipEnabled}
        clickable
      >
        Select the Whisper model.
        <a> </a>
        <a
          className="font-bold underline"
          onClick={() => setTooltipEnabled(false)}
        >
          Close
        </a>
      </Tooltip>
    </>
  );
}

export default YoutubePage;
