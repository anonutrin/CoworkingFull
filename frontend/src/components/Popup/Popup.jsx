import React from 'react';
import s from './Popup.module.css';
import {MdOutlineClose} from "react-icons/md";

function Popup(props) {
    return (props.trigger) ? (
        <div className={s.popup}>
            <div className={s.popupInner}>
                <button className={s.closeBtn} onClick={props.onClose}><MdOutlineClose/></button>
                {props.children}
            </div>
        </div>
    ) : "";
}

export default Popup;
