import React, {useEffect, useState} from 'react';

import "../components/styles.css";

import Loading from "../Assets/Loading/Loading";
import Navbar from "../Assets/Navbar/Navbar";
import Block1 from "../Assets/Home/Block1";
import Block2 from "../Assets/Home/Block2";
import Footer from "../Assets/Footer/Footer";

const Home = () => {
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        setLoading(true)
        setTimeout(() => {
            setLoading(false)
        }, 0)
    }, [])

        return (
            <div className="App_">
            {
                loading ?
                    <Loading />
                    :
                    <div style={{width: "100%", height: "100%", display: "flex", alignItems: "center", flexDirection: "column"}}>
                        <Navbar />
                        <Block1 />
                        <Block2 />
                        <Footer />
                    </div>
            }
            </div>
        );
};

export default Home;