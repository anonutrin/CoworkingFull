import React, {useState} from 'react';
import s from "../LocationCard/LocationCard.module.css";
import t from "./ExtendedLocationCard.module.css";
import '@coreui/coreui/dist/css/coreui.min.css';

import {CButton, CCard, CCardBody, CCollapse} from "@coreui/react";
import Divider from "../../Divider/Divider";
import defaultLocationImage from "../../../assets/images/default_location.png";



function ExtendedLocationCard({id, title, imageUrl, full_address, short_description, price, contact_link, work_schedule, category}) {
    const [visible, setVisible] = useState(false)
    const [imageLink, setImageLink] = useState(imageUrl);
    const photos = [imageLink, imageLink, imageLink, imageLink]
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
  };

    const handleImageError = () => {
        setImageLink(defaultLocationImage);
    };

    return (
        <div key={id} className={s.autoCard}>
            <div className={s.cardImage} onError={handleImageError}>
                <img src={imageLink} alt=""/>
            </div>

            <div className={s.description + " " + t.marginTop5}>
                <h3 className={s.price + " " + s.cardTitle}>{price.replace('руб', '₽') || 0}</h3>
                <div className={t.text + " " + t.titleBLock}>
                    {title}
                </div>
                <div className={t.text}>
                    {work_schedule}
                </div>
                <div className={t.text}>
                    {category}
                </div>
                <div className={t.characterContainer}>
                    <CButton className={t.collapseBtn} href="#" onClick={(event) => {
                        event.preventDefault()
                        setVisible(!visible)
                    }}>
                        Дополнительно
                    </CButton>
                    <Divider height="3px" backgroundColor="gray"/>
                    <CCollapse visible={visible}>
                        <CCard className="mt-3">
                            <CCardBody>
                                {short_description}
                            </CCardBody>
                        </CCard>
                    </CCollapse>
                </div>
                <div className={t.contactBlock + " " + s.width + " needAnimation"}>
                    {contact_link ? <a href={contact_link} target="_blank" className={s.contactLink}>Связаться</a> : ''}
                </div>
            </div>
        </div>
    );
}

export default ExtendedLocationCard;
