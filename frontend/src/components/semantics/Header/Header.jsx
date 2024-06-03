import React, {useEffect, useState} from "react";
import {NavLink} from "react-router-dom";
import s from './Header.module.css';
import Avatar from "../../Avatar/Avatar";
import Title from "../../Title/Title";
import {useTelegram} from "../../../hooks/useTelegram";
import {apiEndpoint} from "../../../api/api"


const Header = () => {
    const {user} = useTelegram();
    const [userInfo, setUserInfo] = useState({});

    useEffect(() => {
        const data = new URLSearchParams();
        if(user?.id)
            data.append('chat_id', user.id);

        fetch(`${apiEndpoint}/user-info?${data.toString()}`)
            .then(response => response.json())
            .then(json => setUserInfo(json))
            .catch(() => {});

    }, [])
    return (
        <header className={s.Header}>
            <div className={s.spaceBlocks}>
                <div className={s.space}>
                    <Avatar avatarUrl={userInfo?.user_photo}/>
                    <NavLink to='/referral' className={s.link}>
                        <div className='flex_col_center'>
                            <span className={s.username}>{user?.username || "Username"}</span>
                            <span className={s.balance}>{userInfo?.balance || 0}р</span>
                        </div>
                    </NavLink>
                    <Title title={"Вся аренда - для твоего мероприятия"}/>
                </div>
                <div className={s.space}>

                </div>
            </div>

        </header>)
}

export default Header;