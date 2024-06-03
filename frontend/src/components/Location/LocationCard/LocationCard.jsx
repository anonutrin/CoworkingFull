import React, {useState} from "react";
import s from './LocationCard.module.css';
import defaultLocationImage from '../../../assets/images/default_location.png';

const LocationCard = ({id, title, imageUrl, full_address, short_description, price, contact_link, work_schedule, category, onAboutClick}) => {
    const [imageLink, setImageLink] = useState(imageUrl);

    const handleImageError = () => {
        setImageLink(defaultLocationImage);
    };

    return (
        <div className={s.locationCard}>
            <div className={s.cardImage}>
                <img src={imageLink} alt="" onError={handleImageError}/>
                <div className={s.locationBlock}>
                    {/*{full_address}*/}
                </div>
            </div>
            <div className={s.description}>
                <div className={s.price + " " + s.cardTitle}>{price.replace('руб', '₽').toLowerCase() || 0}</div>
                <div className={s.titleBLock}>
                    {title}
                </div>

                <button className={s.buttonCard + " needAnimation"} onClick={onAboutClick} data-id={id}>
                    Подробнее
                </button>
            </div>
        </div>
    )
}

export default LocationCard;
