import React from 'react';
import TypeWriterJS from "./nopage";

import "./NoPage.css"

const NoPage = () => {
    return (
        <div className="fzf-error-block">
            <h1 className="fzf-error-text">404</h1>
            <TypeWriterJS></TypeWriterJS>
            {/*<h5 className="fzf-error-desc">Page not found</h5>*/}
        </div>
    );
};

export default NoPage;