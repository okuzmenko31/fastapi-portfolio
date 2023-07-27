import React from 'react';
import './Footer.css';
import { AiFillGithub, AiFillLinkedin, AiFillTwitterCircle } from "react-icons/ai";

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-headers">
                    <h1 style={{margin:"0"}}>OLEG KUZMENKO</h1>
                    <h1 style={{margin:"0"}}>SOCIALS</h1>
                </div>

                <div className="footer-headers-info">
                    <h5 style={{color:"white"}}>Full-time python Back-End Developer</h5>
                    <div className="icons-footer-ok">
                        <a className="link-style" target="_blank" href="#"><AiFillGithub /></a>
                        <a className="link-style" target="_blank" href="#"><AiFillLinkedin /></a>
                        <a className="link-style" target="_blank" href="#"><AiFillTwitterCircle /></a>
                    </div>
                </div>
            </div>

            <hr style={{width: "70%"}}></hr>
            <div className="copyright-footer">
                <h1>© Copyright 2023. Made by <a href="#" className="link-style"><span>Vladyslav Malyshenko</span></a> and <a href="#" className="link-style"><span>Oleg Kuzmenko</span></a></h1>
            </div>

        </footer>
    );
};

export default Footer;