import React from "react";
import {BrowserRouter, BrowserRouter as Router, Route, Routes} from "react-router-dom";

import "./components/styles.css";

import Navbar from "./Assets/Navbar/Navbar";

import Home from "./Pages/Home";
import AboutMe from "./Pages/AboutMe";
import Projects from "./Pages/Projects";
import Blog from "./Pages/Blog";
import SingUp from "./Pages/SingUp";
import SingIn from "./Pages/SingIn";
import NoPage from "./Pages/NoPage";
function App() {

  return (
    <>
    <div className="App">
      <Navbar />
    </div>
      <BrowserRouter>
        <Routes>
          <Route exact path="/Home" element={<Home />}/>
          <Route path="/about" element={<AboutMe />}/>
          <Route path="/projects" element={<Projects />}/>
          <Route path="/blog" element={<Blog />}/>
          <Route path="/singup" element={<SingUp />}/>
          <Route path="/singin" element={<SingIn />}/>
          <Route path="*" element={<NoPage />}/>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
