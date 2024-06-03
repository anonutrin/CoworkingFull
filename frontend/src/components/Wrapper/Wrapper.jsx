import React from "react";
// import s from './Wrapper.module.css';

const Wrapper = ({ children }) => {
    return (
        <div className="App-wrapper">
            <div className="padding-wrapper">
                {children}
            </div>
        </div>
    )
}

export default Wrapper;
