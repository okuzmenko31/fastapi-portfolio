import React from 'react';
import { AiFillGithub } from "react-icons/ai";
import { setToken } from "../../components/Auth"

import "../../components/styles.css";
import "./navbar.css";
import "./navbarbuttons.css";
import "./icons.modules.css";

const Navbar = () => {

    function LogOut() {
        localStorage.removeItem('AuthToken')
    }

    return (
            <div className="navbar">

                <a className="logo" href="http://localhost:3000">OK</a>

                <div className="navbar-main-block">
                    <div className="navigation-block">
                        <a className="navbar-button" href="/">Home</a>
                        <a className="navbar-button" href="/about">About me</a>
                        <a className="navbar-button" href="/projects">Projects</a>
                        <a className="navbar-button" href="/blog">Blog</a>
                        <a className="navbar-button icons" href="#"><AiFillGithub /></a>
                    </div>
                    <div className="registration-sing-in-block">
                        {
                            !localStorage.getItem("AuthToken") ?
                                <>
                                    <a className="navbar-button" href="/singin">Sing in</a>
                                    <a className="navbar-button" href="/singup">Sing up</a>
                                </>
                                :
                                <a className="navbar-button" onClick={LogOut} href="/singin">Log Out</a>
                        }
                    </div>
                </div>
            </div>
    );
};

export default Navbar;