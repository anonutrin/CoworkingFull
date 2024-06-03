import React from "react";
import s from './Title.module.css';


const Title = ({title}) => {

    return (
        <div className={s.title}>{title}</div>
    )
}

export default Title;