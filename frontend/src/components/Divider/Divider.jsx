import React from "react";
import s from './Divider.module.css';


const Divider = ({height, backgroundColor}) => {
    const styles = {"height": height || "1px", "backgroundColor": backgroundColor || "#f5f5f5"}
    return (
        <div className={s.divider} style={styles}></div>
    )
}

export default Divider;