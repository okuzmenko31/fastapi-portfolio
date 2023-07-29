import React, { useState } from 'react';

import "../../components/styles.css"
import "./singup.css"

import beautifulImage from "../../components/imgs/beautifulImage.png"
import { CSSTransition } from "react-transition-group";
import Footer from "../../Assets/Footer/Footer";


const SingUp = () => {
    const [showSecretPhraseField, setShowSecretPhraseField] = useState(false);

    const toggleSecretPhraseField = () => {
        setShowSecretPhraseField(!showSecretPhraseField);
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
                                            <input className="reg-input" placeholder="Please enter an username"/>
                                        </div>
                                        <div className="singup-form-block">
                                            <h5>Email</h5>
                                            <input className="reg-input" placeholder="Please enter an email"/>
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
                                                <input className="reg-input" placeholder="Please enter a secret phrase" />
                                            </CSSTransition>
                                        </div>
                                    </div>
                                    <div className="singup-forms-form-right">
                                        <div className="singup-form-block">
                                            <h5>Password</h5>
                                            <input className="reg-input" placeholder="Please enter a password"/>
                                        </div>
                                        <div className="singup-form-block">
                                            <h5>Confirm password</h5>
                                            <input className="reg-input" placeholder="Please confirm your password"/>
                                        </div>
                                        <div className="show-secret-phrase-field">
                                            <h5 style={{margin:"0px"}}>As Admin</h5>
                                            <input className="secret-phrase-checkbox" style={{ margin: "0 0 0 10px" }} type="checkbox" onChange={toggleSecretPhraseField} checked={showSecretPhraseField}
                                            />
                                        </div>
                                    </div>
                                </div>

                                <button className="form-button-submit">
                                    Submit
                                </button>
                                <h5 style={{color:"lightgray", marginTop:"30px"}}>Already have an account? <a className="font-color-link" href="/singin">Sing in!</a></h5>
                            </form>
                        </div>
                    </div>
                </div>
    );
};

export default SingUp;