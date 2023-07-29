import React from "react";
import Typewriter from "typewriter-effect";

function Type() {
    return (
        <Typewriter
            options={{
                strings: [
                    "Freelancer",
                    "Back-End Developer",
                    "Crypto Enthusiast",
                ],
                autoStart: true,
                loop: true,
                deleteSpeed: 50,
                wrapperClassName:"TypeText",
                cursorClassName:"TypeText",
            }}
        />
    );
}

export default Type;