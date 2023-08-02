import React, {useState} from 'react';
import beautifulImage from "../../components/imgs/beautifulImage.png";
import { AiOutlineEye as Eye, AiOutlineEyeInvisible as EyeInv } from "react-icons/ai";

import "./singin.css"
import axios from "axios";
import { setToken } from '../../components/Auth'

const SingIn = () => {
    const [authValue, setAuthValue] = useState("");
    const [password, setPassword] = useState("")
    const [passVisible, setPassVisible] = useState(false)
    const [errorMessage, setErrorMessage] = useState("");

    function log_user() {
        axios.post('http://localhost:8000/auth/login/', {
            "auth_value":authValue,
            "password":password
        })
            .then(response => {
                setToken(response.data.access_token)
            })
            .catch(function (error) {
                if (typeof error.response.data.detail === "object") {
                    const arrayError = error.response.data.detail[0].msg;
                    setErrorMessage(arrayError);
                } else {
                    const defaultError = error.response.data.detail;
                    setErrorMessage(defaultError);
                }
            });
    }

    return (
        <div className="singin-window high_index">
            <div className="singin-img">
                <img style={{width:"100%", height:"100%"}} alt="" src={beautifulImage} />
            </div>

            <div className="singin-forms">
                <h1 className="singin-title">Authorization</h1>
                <div className="singin-block">

                    <form className="singin-forms-form">
                        <div className="singin-forms-form-block">
                            <div className="singin-forms-form-left">
                                <div className="singin-form-block">
                                    <h5>Username or email</h5>
                                    <input value={authValue} onChange={e => setAuthValue(e.target.value)} className="sin-input" placeholder="Please enter your username or email"/>
                                </div>
                                </div>
                                <div className="singin-forms-form-right">
                                    <div className="singin-form-block">
                                        <h5>Password</h5>
                                        <div  style={{display:"flex", alignItems:"center", justifyContent:"end"}}>
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
                                </div>
                        </div>

                        <button type="button" onClick={log_user} className="form-button-submit">
                            Submit
                        </button>
                        {errorMessage && <h5 style={{ color: "red" }}>{errorMessage}</h5>}
                        <h5 style={{color:"lightgray", marginTop:"30px"}}>Don't have an account? <a className="font-color-link" href="/singup">Sing up!</a></h5>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default SingIn;