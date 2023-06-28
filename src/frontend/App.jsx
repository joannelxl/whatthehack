import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import React from "react";
import MainNavBar from "./components/MainNavBar";
import URLQueryPage from "./pages/URLQueryPage";
import LocalSementicSearchPage from "./pages/LocalSementicSearchPage";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <MainNavBar />
        <Routes>
          <Route path="/home/" element={<HomePage />} />
          <Route path="/urlquery/" element={<URLQueryPage />} />
          <Route
            path="/localsementicsearch/"
            element={<LocalSementicSearchPage />}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
