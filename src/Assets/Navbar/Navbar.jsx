import React from 'react';
import { AiFillGithub } from "react-icons/ai";

import "../../components/styles.css";
import "./navbar.css";
import "./navbarbuttons.css";
import "./icons.modules.css";

const Navbar = () => {
    return (
            <div className="navbar">

                <a className="logo" href="http://localhost:3000">OK</a>

                <div className="navbar-main-block">
                    <div className="navigation-block">
                        <a className="navbar-button" href="/home">Home</a>
                        <a className="navbar-button" href="/about">About me</a>
                        <a className="navbar-button" href="/projects">Projects</a>
                        <a className="navbar-button" href="/blog">Blog</a>
                        <a className="navbar-button icons" href="#"><AiFillGithub /></a>
                    </div>
                    <div className="registration-sing-in-block">
                        <a className="navbar-button" href="/singup">Sing up</a>
                        <a className="navbar-button" href="/singin">Sing in</a>
                    </div>
                </div>
            </div>
    );
};

export default Navbar;