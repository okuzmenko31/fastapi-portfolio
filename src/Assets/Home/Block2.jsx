import React from 'react';
import "../../components/styles.css"
import "./Block2.css"
import Tilt from "react-parallax-tilt";

const Block2 = () => {
    return (
        <div className="block-2 high_index">
            <div className="block-2-info high_index">
                <div className="block2-introduce-info">
                    <h1 style={{fontSize:"60px", fontWeight:"bold"}} className="no-margin-to-bottom">Let me <span className="choosed-text">introduce</span> myself!</h1>
                    <h3>I fell in love with programming and I have at least learnt something, I think… 🤷‍♂️</h3>
                    <h3>I am fluent in classics like C++, Javascript and Go.</h3>
                    <h3>My field of Interest's are building new  Web Technologies and Products and also in areas related to Blockchain.</h3>
                    <h3>Whenever possible, I also apply my passion for developing products with Node.js and Modern Javascript Library and Frameworks  like React.js and Next.js</h3>
                </div>
            </div>
            <div className="block2-interactive-img">
                <Tilt>
                    <img src="https://soumyajit.vercel.app/static/media/avatar.5852f40fbb38aa284829fa3fb7722225.svg" />
                </Tilt>
            </div>
        </div>
    );
};

export default Block2;