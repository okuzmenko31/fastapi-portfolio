import React from 'react';
import Typewriter from "typewriter-effect";

const Nopage = () => {
    return (
        <Typewriter
            options={{
                strings: [
                    "Page not found",
                ],
                autoStart: true,
                loop: true,
                deleteSpeed: 50,
                wrapperClassName:"fzf-error-desc typewritter-text-color",
                cursorClassName:"fzf-error-desc typewritter-text-color",
            }}
        />
    );
};

export default Nopage;