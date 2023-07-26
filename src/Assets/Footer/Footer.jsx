import React from 'react';
import classes from './Footer.css';
import { AiFillGithub, AiFillLinkedin, AiFillTwitterCircle } from "react-icons/ai";

const Footer = () => {
    return (
        <div className="footer">
            <div className="footer-content">
                <div className="info-footer">
                    <h1>OLEG KUZMENKO</h1>
                    <h5>Full-time python Back-End Developer</h5>
                </div>

                <div className="socials-footer">
                    <h1>SOCIALS</h1>
                    <div className="icons-footer">
                        <a className="link-style" target="_blank" href="https://github.com/okuzmenko31"><AiFillGithub /></a>
                        <a className="link-style" target="_blank" href="#"><AiFillLinkedin /></a>
                        <a className="link-style" target="_blank" href="#"><AiFillTwitterCircle /></a>
                    </div>
                </div>
            </div>

            <hr style={{width: "70%"}}></hr>
            <div className="copyright-footer">
                <h1>© Copyright 2023. Made by <a href="#" className="link-style"><span>Vladyslav Malyshenko</span></a> and <a href="#" className="link-style"><span>Oleg Kuzmenko</span></a></h1>
            </div>

        </div>
    );
};

export default Footer;