import React from "react";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";

import "./components/styles.css";

import Navbar from "./Assets/Navbar/Navbar"

import Home from "./Pages/Home/Home";
import AboutMe from "./Pages/AboutMe/AboutMe";
import Projects from "./Pages/Projects/Projects";
import Blog from "./Pages/Blog/Blog";
import SingUp from "./Pages/SingUp/SingUp";
import SingIn from "./Pages/SingIn/SingIn";
import NoPage from "./Pages/NoPage/NoPage";
import Footer from "./Assets/Footer/Footer";
function App() {

  return (
    <>
    <div className="App">
      {
        <BrowserRouter>
          <Routes>
            <Route path="/Home" element={<Home />}/>
            <Route path="/about" element={<AboutMe />}/>
            <Route path="/projects" element={<Projects />}/>
            <Route path="/blog" element={<Blog />}/>
            <Route path="/singup" element={<SingUp />}/>
            <Route path="/singin" element={<SingIn />}/>
            <Route path="*" element={<NoPage />}/>
            <Route path="/" element={ <Navigate to="/home" /> } />
          </Routes>
        </BrowserRouter>
      }
      <Navbar />
    </div>
    </>
  );
}

export default App;
