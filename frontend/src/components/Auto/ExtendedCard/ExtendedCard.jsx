import React, {useState} from 'react';
import s from "../AutoCard/AutoCard.module.css";
import t from "./ExtendedCard.module.css";
import '@coreui/coreui/dist/css/coreui.min.css';

import {CButton, CCard, CCardBody, CCollapse} from "@coreui/react";
import Divider from "../../Divider/Divider";
import { FaPhoneAlt } from "react-icons/fa";
import { FaInstagram, FaViber  } from "react-icons/fa";
import { FaTelegram, FaWhatsapp  } from "react-icons/fa6";
import defaultLocationImage from "../../../assets/images/default_location.png";


function ExtendedCard({id, brand, model, equipment, year_of_issue, class_type, color, body, drive_unit, fuel_type, transmission, power, volume_engine, fuel_volume, acceleration_to100, seats_number, city, rent_cost_per_day, rent_cost_per_month, description, links, imageUrl}) {
    const [visible, setVisible] = useState(false)
    const [imageLink, setImageLink] = useState(imageUrl);

    const handleImageError = () => {
        setImageLink(defaultLocationImage);
    };

    return (
        <div className={s.autoCard}>
            <div className={s.cardImage}>
                <img src={imageLink} alt="" onError={handleImageError}/>
            </div>
            <div className={s.description + " " + t.marginTop5}>
                <h3 className={s.price + " " + s.cardTitle}>{rent_cost_per_day.replace('руб', '₽') || 0}</h3>
                <div className={t.text}>
                    {brand} {model}
                </div>
                <div className={t.characterContainer}>
                    <CButton className={t.collapseBtn} href="#" onClick={(event) => {
                        event.preventDefault()
                        setVisible(!visible)
                    }}>
                        Характеристики
                    </CButton>
                    <Divider height="3px" backgroundColor="gray"/>
                    <CCollapse visible={visible}>
                        <CCard className="mt-3">
                            <CCardBody>
                                <div>Екипировка: {equipment}</div>
                            </CCardBody>
                        </CCard>
                    </CCollapse>
                </div>
                <div className={t.contactBlock}>
                    <h6> Номер телефона: </h6>
                    <FaPhoneAlt size="18px"/>
                    <span>+99999999999</span>
                    <br/><br/>
                    <span>Социальные сети:</span><br/>
                    <div className={t.socialNetworks}>
                        <FaInstagram size="30px" />
                        <FaTelegram size="30px" />
                        <FaViber size="30px" />
                        <FaWhatsapp size="30px" />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ExtendedCard;
