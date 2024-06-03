import React from "react";
import s from './Avatar.module.css';
import defaultAvatar from '../../assets/images/avatar_template.jpg';

const Avatar = ({avatarUrl}) => {

    return (
        <div className={s.Avatar}>
            <img src={avatarUrl || defaultAvatar} alt="Ava"/>
        </div>
    )
}

export default Avatar;