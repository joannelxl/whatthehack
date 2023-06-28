import React from "react";
import { MainNavBarData } from "./MainNavBarData";
import "./MainNavBar.css";
import DXClogo from "../assets/dxc-brand.png";

function MainNavBar() {
  return (
    <div className="sidebar">
      <div className="main-logo-area">
        <img src={DXClogo} className="img" />
      </div>
      <ul className="sidebar-list">
        {MainNavBarData.map((val, key) => {
          return (
            <li
              key={key}
              className={
                val.title == "BETA (under development)" ? "special-row" : "row"
              }
              id={
                window.location.pathname.split("/").slice(-2)[0] == val.link
                  ? "active"
                  : ""
              }
              onClick={() => {
                let pagePath = "/" + val.link;
                let userPath = "/" + window.location.pathname.split("/").pop();
                let newPath = pagePath.concat(userPath);
                window.location.pathname = newPath;
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
