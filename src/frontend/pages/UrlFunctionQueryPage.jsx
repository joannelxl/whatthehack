import React, { useState, useEffect } from "react";
import Select from "react-select";
import { Tooltip } from "react-tooltip";
import Moment from "moment";
import axios from "axios";

import "./UrlFunctionQueryPage.css";
import "../App.css";
import "react-toastify/dist/ReactToastify.css";
import "react-tooltip/dist/react-tooltip.css";
import "viewerjs/dist/viewer.css";
import "bootstrap/dist/css/bootstrap.min.css";

import { ThreeDots } from "react-loader-spinner";
import HelpOutlineOutlinedIcon from "@mui/icons-material/HelpOutlineOutlined";

function UrlFunctionQueryPage() {
  // default model is GPT 3.5
  const [selectedModel, setSelectedModel] = useState({
    value: "gpt-35",
    label: "GPT-3.5",
  });

  // default function is Summarization
  const [func, setFunc] = useState({
    value: "summarize",
    label: "Summarization",
  });

  const [inputLanguage, setInputLanguage] = useState("English");
  const [updatedLanguage, setUpdatedLanguage] = useState(inputLanguage);
  const [user, setUser] = useState(
    window.location.pathname.split("/").pop() === "9" ? "9" : "default"
  );
  const [url, setUrl] = useState(null);
  const [response, setResponse] = useState(null);
  const [completedStatus, setCompletedStatus] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState(false);

  const [tooltipEnabled, setTooltipEnabled] = useState(false);

  // 3 functions
  const functions = [
    { value: "summarize", label: "Summarization" },
    { value: "keyword", label: "Keyword Extraction" },
    { value: "translate", label: "Translation " },
  ];

  // GPT models
  const models = [
    { value: "gpt-35", label: "GPT-3.5" },
    { value: "gpt-4-8k", label: "GPT-4-8k" },
    { value: "gpt-4-32k", label: "GPT-4-32k" },
  ];

  // ******************************************** Event Handlers********************************************

  // set input language upon user input
  function handleLangChange(e) {
    setInputLanguage(e.target.value);
  }

  // set updated language when user clicks Change button
  function handleLangClick() {
    setUpdatedLanguage(inputLanguage);
  }

  // clear the file
  function clearFile() {
    setCompletedStatus(false);
  }

  // upon url submission
  function handleRun(e) {
    e.preventDefault();
    submitQuery(
      `https://dxclnvmonline2.eastus.cloudapp.azure.com:8080/${func.value}`,
      {
        url: url,
        user: user,
        model: selectedModel.value,
        language: updatedLanguage,
        headers: {
          "Access-Control-Allow-Headers": "Content-Type",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin":
            "https://polite-mud-0e3eb4d10.2.azurestaticapps.net",
          "Access-Control-Allow-Credentials": "true",
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

  // clear text input, reset url, reset language
  function handleClear(e) {
    let urlInput = document.getElementById("url-input");
    urlInput.value = null;
    setUrl(null);
    setLoadingStatus(false);
    setCompletedStatus(false);
    setUpdatedLanguage("English");
    let langInput = document.getElementById("lang-input");
    langInput.value = null;
  }

  // download file upon button click
  function handleDownload(e) {
    exportFile(response);
  }

  // function to write to file
  function exportFile(fileContent) {
    if (fileContent.at(0) === '"' && fileContent.at(-1) === '"') {
      fileContent = fileContent.slice(1, -1);
    }
    const element = document.createElement("a");
    const file = new Blob([fileContent], { type: "text/plain" });
    element.href = window.URL.createObjectURL(file);
    let name = "";

    // naming for files based on their function
    switch (func.value) {
      case "summarize":
        name = "sum";
        break;
      case "keyword":
        name = "key";
        break;
      case "translate":
        name = "tra";
        break;
    }

    element.download =
      "url_" + name + "_" + Moment().format("MMDDhhmmss") + ".txt";
    document.body.appendChild(element);
    element.click();
  }

  // ******************************************** API Fetch Functions********************************************

  // send request to get text from url API through axios
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
    <div>
      <div class="combinedurlquerypage-content">
        <div class="combinedurlquery-top-bar">
          <div class="btn-group">
            {/* show user guide button */}
            <button
              type="button"
              onClick={() => {
                setTooltipEnabled(true);
              }}
            >
              <HelpOutlineOutlinedIcon class="btn-icon" />
              <span class="btn-text"> Show User Guide </span>
            </button>
          </div>
          <div class="select-btn">
            <span class="select-text"> Select model: </span>
            <Select
              id="select-model"
              defaultValue={selectedModel}
              onChange={setSelectedModel}
              options={models}
              placeholder="Select Model"
            />
          </div>
        </div>
        <div class="url-main-content">
          <br></br>
          <br></br>
          <h2 className="text-2xl font-bold self-center">
            Summarize / Extract Keywords from / Translate your webpage
          </h2>
          <br></br>
          <br></br>
          <div className="flex flex-col">
            <div className="flex justify-center">
              <Select
                id="select-func"
                defaultValue={func}
                onChange={(e) => {
                  setFunc(e);
                  clearFile();
                }}
                options={functions}
                placeholder="Select Function"
                className="mx-2 text-sm"
              />
            </div>
            <br></br>
            {func.value == "translate" && (
              <div className="flex flex-row w-full items-center justify-center">
                <label className="pr-2">
                  Translate to {updatedLanguage} or translate to another
                  language:
                </label>
                <input
                  type="text"
                  placeholder="Input a language"
                  id="lang-input"
                  onChange={handleLangChange}
                  className="w-fit px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400
                            focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                />
                <button
                  className="rounded-md bg-gray-200 text-[#000000] w-fit mx-2"
                  onClick={handleLangClick}
                  id="enter-language"
                >
                  Change
                </button>
              </div>
            )}
            <br></br>
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
            <div className="flex justify-center">
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
      <div>
        <Tooltip
          anchorSelect="#url-input"
          variant="info"
          isOpen={tooltipEnabled}
          clickable
        >
          Enter your URL here. Click Run to submit.
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
          anchorSelect="#select-func"
          variant="info"
          isOpen={tooltipEnabled}
          clickable
        >
          Select the function.
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
          Select the GPT model.
          <a> </a>
          <a
            className="font-bold underline"
            onClick={() => setTooltipEnabled(false)}
          >
            Close
          </a>
        </Tooltip>
      </div>
    </div>
  );
}

export default UrlFunctionQueryPage;
