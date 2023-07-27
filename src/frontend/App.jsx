import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import React from "react";
import MainNavBar from "./components/MainNavBar";
import UrlFunctionQueryPage from "./pages/UrlFunctionQueryPage";
import LocalSementicSearchPage from "./pages/LocalSementicSearchPage";
import YoutubePage from "./pages/YoutubePage";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <MainNavBar />
        <Routes>
          <Route path="/home" element={<HomePage />} />
          <Route path="/urlquery" element={<UrlFunctionQueryPage />} />
          <Route
            path="/localsementicsearch"
            element={<LocalSementicSearchPage />}
          />
          <Route path="/youtube" element={<YoutubePage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
