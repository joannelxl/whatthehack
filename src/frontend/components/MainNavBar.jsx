import React from "react";
import { MainNavBarData } from "./MainNavBarData";
import "./MainNavBar.css";
import DXClogo from '../assets/robot2.jpg';

function MainNavBar() {
  return (
    <div className="sidebar">
      <div className="main-logo-area">
        <img src={DXClogo} className="img-logo" alt="robot" />

      </div>
      <ul className="sidebar-list">
        {MainNavBarData.map((val, key) => {
          return (
            <li
              key={key}
              className="row"
              id={
                // set different colour for currently active page
                window.location.pathname.split("/").pop == val.link
                  ? "active"
                  : ""
              }
              onClick={() => {
                let pagePath = "/" + val.link; // path to selected page
                window.location.pathname = pagePath;
              }}
            >
              <div id="icon"> {val.icon} </div>
              <div id="title"> {val.title} </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default MainNavBar;
