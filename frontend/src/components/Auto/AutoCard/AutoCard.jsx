import React, {useState} from "react";
import s from './AutoCard.module.css';
import defaultLocationImage from "../../../assets/images/default_location.png";

const AutoCard = ({id, brand, model, equipment, year_of_issue, class_type, color, body, drive_unit, fuel_type, transmission, power, volume_engine, fuel_volume, acceleration_to100, seats_number, city, rent_cost_per_day, rent_cost_per_month, description, links, imageUrl, onAboutClick}) => {
    const [imageLink, setImageLink] = useState(imageUrl);

    const handleImageError = () => {
        setImageLink(defaultLocationImage);
    };

    return (
        <div className={s.autoCard}>
            <div className={s.cardImage}>
                <img src={imageLink} alt="" onError={handleImageError}/>
            </div>
            <div className={s.description}>
                <div className={s.price + " " + s.cardTitle}>{rent_cost_per_day.replace('руб', '₽') || 0}</div>
                <div>
                    {brand} {model}
                </div>
                <button className={s.buttonCard + " needAnimation"} onClick={onAboutClick} data-id={id}>
                    Подробнее
                </button>
            </div>
        </div>
    )
}

export default AutoCard;
