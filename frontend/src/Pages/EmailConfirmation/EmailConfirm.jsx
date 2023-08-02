import React, {useState} from 'react';
import { useParams } from "react-router-dom";
import axios from "axios"

import beautifulImage from "../../components/imgs/beautifulImage.png";
import "./EmailConfirm_.css"
import {email} from "../SingUp/SingUp"
import {AiOutlineCheck} from "react-icons/ai";

const EmailConfirm = () => {
    const [modalWinVis, setModalWinVis] = useState(false);
    const emailText = document.querySelector("#email-mod-text");
    const [errorMessage, setErrorMessage] = useState("");
    const params = useParams()

    function submitConfirmEmail() {
        let token = params.token
        let email = params.email
        axios.post(`http://localhost:8000/auth/confirm_email_and_set_active/${token}/${email}/`, {
        })
            .then(async response => {
                console.log(response);
                emailText.innerHTML = await(response.data.detail);
                setModalWinVis(true)
            })
            .catch(function (error) {
                const defaultError = error.response.data.detail;
                setErrorMessage(defaultError);
            });
    }

    return (
        <div className="confirm-window high_index">
            <div className="confirm-img">
                <img style={{width:"100%", height:"100%"}} alt="" src={beautifulImage} />
            </div>

            <div className="confirm-forms">
                <h1 className="confirm-title">Email Confirmation</h1>
                <div className="confirm-block">
                    <h5>Your emails is: {params.email}</h5>
                    <button type="button" onClick={submitConfirmEmail} className="form-button-submit">
                        Confirm email
                    </button>
                    {errorMessage && <h5 style={{ color: "red" }}>{errorMessage}</h5>}
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

export default EmailConfirm;