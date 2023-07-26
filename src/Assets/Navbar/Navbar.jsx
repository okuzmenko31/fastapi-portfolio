import React from 'react';
import DefaultStyles from "../../components/styles.css";
import classes from "./navbar.css";
import cls from "./navbarbuttons.css";
import cls2 from "./icons.modules.css";
import { AiFillGithub } from "react-icons/ai";

const Navbar = () => {
    return (
        <div className="navbar">

            <a className="logo" href="http://localhost:3000">OK</a>

            <div className="navigation-block">
                <a className="navbar-button" href="http://localhost:3000">Home</a>
                <a className="navbar-button" href="http://localhost:3000">About me</a>
                <a className="navbar-button" href="http://localhost:3000">Projects</a>
                <a className="navbar-button" href="http://localhost:3000">Blog</a>
                <a className="navbar-button icons" href="#"><AiFillGithub /></a>
            </div>
        </div>
    );
};

export default Navbar;