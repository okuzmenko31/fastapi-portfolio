import React from 'react';
import classes from './Footer.css';
import { AiFillGithub, AiFillLinkedin, AiFillTwitterCircle } from "react-icons/ai";

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="info-footer">
                    <h1>OLEG KUZMENKO</h1>
                    <h5>Full-time python Back-End Developer</h5>
                </div>

                <div className="socials-footer">
                    <h1 style={{marginTop: "0", marginBottom: "0"}}>SOCIALS</h1>
                    <div className="icons-footer-ok">
                        <h5 style={{marginTop: "0", marginBottom: "0"}}>Oleg Kuzmenko</h5>
                        <div className="icons-ft">
                            <a className="link-style" target="_blank" href="#"><AiFillGithub /></a>
                            <a className="link-style" target="_blank" href="#"><AiFillLinkedin /></a>
                            <a className="link-style" target="_blank" href="#"><AiFillTwitterCircle /></a>
                        </div>
                    </div>
                    <div className="icons-footer-vm">
                        <h5 style={{marginTop: "0", marginBottom: "0"}}>Vladyslav Malyshenko</h5>
                        <div className="icons-ft">
                            <a className="link-style" target="_blank" href="#"><AiFillGithub /></a>
                            <a className="link-style" target="_blank" href="#"><AiFillLinkedin /></a>
                            <a className="link-style" target="_blank" href="#"><AiFillTwitterCircle /></a>
                        </div>
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