import React, { useState } from 'react';
import { AiOutlineEye as Eye, AiOutlineEyeInvisible as EyeInv, AiOutlineCheck } from "react-icons/ai";
import axios from "axios"

import "../../components/styles.css"
import "./singup.css"

import beautifulImage from "../../components/imgs/beautifulImage.png"
import { CSSTransition } from "react-transition-group";


const SingUp = () => {
    const [showSecretPhraseField, setShowSecretPhraseField] = useState(false);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirm_password, setConfirmPassword] = useState("");
    const [secret_phrase, setSecretPhrase] = useState("");
    const [passVisible, setPassVisible] = useState(false);
    const [modalWinVis, setModalWinVis] = useState(false);
    const errorElem = document.querySelector("#error-text")
    const emailText = document.querySelector("#email-mod-text")

    function reg_user() {
        axios.post('http://localhost:8000/auth/registration/', {
            "username":username,
            "email":email,
            "password":password,
            "password_confirmation":confirm_password
        })
            .then(async response => {
                emailText.innerHTML = await(response.data.message);
                setModalWinVis(true)
            })
            .catch(function (error) {
                function checkErrorType() {
                    if (typeof error.response.data.detail === "object") {
                        errorElem.innerHTML = error.response.data.detail[0].msg
                    } else {
                        errorElem.innerHTML = error.response.data.detail
                    }
                }
                checkErrorType()
            });
    }
//error.response.data.detail
    function reg_user_admin() {
        axios.post('http://localhost:8000/auth/registration/', {
            "username":username,
            "email":email,
            "password":password,
            "password_confirmation":confirm_password,
            "secret_phrase": secret_phrase
        })
            .then(async response => {
                emailText.innerHTML = await(response.data.message);
                setModalWinVis(true)
            })
            .catch(error  => {
                console.log(error);
                function checkErrorType() {
                    if (typeof error.response.data.detail === "object") {
                        errorElem.innerHTML = error.response.data.detail[0].msg
                    } else {
                        errorElem.innerHTML = error.response.data.detail
                    }
                }
                checkErrorType()
            });
    }

    const toggleSecretPhraseField = () => {
        setShowSecretPhraseField(!showSecretPhraseField);
    };

    const togglePasswordVisibility = () => {
        setPassVisible(!passVisible);
    };

    return (
                <div className="singup-window high_index">
                    <div className="singup-img">
                        <img style={{width:"100%", height:"100%"}} alt="" src={beautifulImage} />
                    </div>

                    <div className="singup-forms">
                        <h1 className="registration-title">Registration</h1>
                        <div className="singup-block">

                            <form className="singup-forms-form">
                                <div className="singup-forms-form-block">
                                    <div className="singup-forms-form-left">
                                        <div className="singup-form-block">
                                            <h5>Username</h5>
                                            <input value={username} onChange={e => setUsername(e.target.value)} className="reg-input" placeholder="Please enter an username"/>
                                        </div>
                                        <div className="singup-form-block">
                                            <h5>Email</h5>
                                            <input value={email} onChange={e => setEmail(e.target.value)} className="reg-input" placeholder="Please enter an email"/>
                                        </div>
                                        <div className="singup-form-block admin-field">
                                            <CSSTransition
                                                in={showSecretPhraseField}
                                                timeout={1000}
                                                classNames="admin-field"
                                                unmountOnExit
                                            >
                                                <h5>Secret phrase</h5>
                                            </CSSTransition>
                                            <CSSTransition
                                                in={showSecretPhraseField}
                                                timeout={1000}
                                                classNames="admin-field"
                                                unmountOnExit
                                            >
                                                <input value={secret_phrase} onChange={e => setSecretPhrase(e.target.value)} className="reg-input" placeholder="Please enter a secret phrase" />
                                            </CSSTransition>
                                        </div>
                                    </div>
                                    <div className="singup-forms-form-right">
                                        <div className="singup-form-block">
                                            <h5>Password</h5>
                                            <div style={{display:"flex", alignItems:"center", justifyContent:"end"}}>
                                                <input id="password"
                                                       value={password}
                                                       type={passVisible ? "text" : "password"}
                                                       onChange={e => setPassword(e.target.value)}
                                                       className={!passVisible ? "reg-input password-font" : "reg-input"}
                                                       placeholder="Please enter a password"
                                                />
                                                <div style={{position:"absolute", padding:"10px", margin:"0", width:"16px", height:"16px", cursor:"pointer"}}
                                                     onClick={() => {
                                                         setPassVisible(!passVisible)
                                                     }}>
                                                    {
                                                        passVisible ? <Eye /> : <EyeInv />
                                                    }
                                                </div>
                                            </div>
                                        </div>
                                        <div className="singup-form-block">
                                            <h5>Confirm password</h5>
                                            <input id="confirm_password"
                                                   value={confirm_password}
                                                   type={passVisible ? "text" : "password"}
                                                   onChange={e => setConfirmPassword(e.target.value)}
                                                   className={!passVisible ? "reg-input password-font" : "reg-input"}
                                                   placeholder="Please confirm your password"
                                            />
                                        </div>
                                        <div className="show-secret-phrase-field">
                                            <h5 style={{margin:"0px"}}>As Admin</h5>
                                            <input className="secret-phrase-checkbox" style={{ margin: "0 0 0 10px" }} type="checkbox" onChange={toggleSecretPhraseField} checked={showSecretPhraseField}
                                            />
                                        </div>
                                    </div>
                                </div>

                                <button type="button" onClick={
                                    showSecretPhraseField === true ?
                                    reg_user_admin :
                                    reg_user
                                } className="form-button-submit">
                                    Submit
                                </button>
                                <h5 style={{color:"red"}} id="error-text" content="" />
                                <h5 style={{color:"lightgray", marginTop:"30px"}}>Already have an account? <a className="font-color-link" href="/singin">Sing in!</a></h5>
                            </form>
                        </div>
                    </div>
                    <div id="modal-window-container" style={{
                        opacity: modalWinVis ? "1" : "0",
                        pointerEvents: modalWinVis ? "all" : "none"
                    }}>
                        <div className="modal-window">
                            <AiOutlineCheck className="modal-window-icon"/>
                            <h2>Successful registration!</h2>
                            <h5 id="email-mod-text" content=""/>
                            <button id="modal-window-button" onClick={() => {
                                setModalWinVis(false)
                            }}>OK, Close</button>
                        </div>
                    </div>
                </div>
    );
};

export default SingUp;