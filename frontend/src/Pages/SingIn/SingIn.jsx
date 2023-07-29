import React, {useState} from 'react';
import beautifulImage from "../../components/imgs/beautifulImage.png";
import "./singin.css"

const SingIn = () => {
    const [password, setPassword] = useState("")
    const [passVisible, setPassVisible] = useState(false)

    const togglePasswordVisibility = () => {
        setPassVisible(!passVisible);
    };

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
                                    <input className="sin-input" placeholder="Please enter your username or email"/>
                                </div>
                                </div>
                                <div className="singin-forms-form-right">
                                    <div className="singin-form-block">
                                        <div style={{display:"flex"}}>
                                            <h5>Password</h5>
                                            <input className="setPassVisibility" style={{ margin: "0 0 0 10px" }} type="checkbox" onChange={togglePasswordVisibility} checked={passVisible}/>
                                        </div>
                                        <input id="password"
                                               value={password}
                                               type={passVisible ? "text" : "password"}
                                               onChange={e => setPassword(e.target.value)}
                                               className={!passVisible ? "reg-input password-font" : "reg-input"}
                                               placeholder="Please enter a password"
                                        />
                                    </div>
                                </div>
                        </div>

                        <button className="form-button-submit">
                            Submit
                        </button>
                        <h5 style={{color:"lightgray", marginTop:"30px"}}>Don't have an account? <a className="font-color-link" href="/singup">Sing up!</a></h5>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default SingIn;