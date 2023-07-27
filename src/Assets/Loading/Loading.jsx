import React from 'react';
import "../../components/styles.css"
import "./Loading.css"

const Loading = () => {
    return (
        <div className="loading-block highest-index">
            <h2 className="loading-text" data-text="Developing...">Developing...</h2>
        </div>
    );
};

export default Loading;