import React, {useEffect, useState} from "react";
import s from './Auto.module.css';
import AutoCard from "./AutoCard/AutoCard";
import {useTelegram} from "../../hooks/useTelegram";
import Popup from "../Popup/Popup";
import ExtendedCard from "./ExtendedCard/ExtendedCard";
import {fetchAutos} from "../../api/api";

const Auto = () => {
    const [autos, setAutos] = useState([]);
    const [autosSize, setAutosSize] = useState(0);
    const [selectedProduct, setSelectedProduct] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const {showBackButton, toMain} = useTelegram()


    useEffect(() => {
        showBackButton(toMain);
    }, [])

    useEffect(() => {
        const loadAutos = async () => {
            try {
                const { data, totalAuto } = await fetchAutos(currentPage);
                setAutosSize(totalAuto);
                setAutos((prevAutos) => {
                    const newData = data.filter(newAuto => !prevAutos.some(prevAuto => prevAuto.id === newAuto.id));
                    return [...prevAutos, ...newData];
                });
            } catch (error) {
                console.error("Error fetching autos:", error);
            }
        };
        loadAutos();

    }, [currentPage]);

    const handleProductButtonClick = (event) => {
        const productId = event.target.dataset.id;
        setSelectedProduct(productId);
    };
    const onClose = () => {
        setSelectedProduct(null);
    }
    const getProductById = (productId) => {
        return autos.find((product) => {
            return product.id === +productId;
        }) || {}
    }
    const loadMoreAutos = () => {
        setCurrentPage((prevPage) => prevPage + 1);
    };

    return (
        <>
            <div className={s.autoBlock}>
                <div className={s.mainTitle}>Поможем подобрать автомобиль</div>
                <div className={s.cardsBlock}>
                    {autos.map(auto => (
                        <AutoCard
                            key={auto.id}
                            brand={auto.brand}
                            equipment={auto.equipment}
                            year_of_issue={auto.year_of_issue}
                            class_type={auto.class_type}
                            color={auto.color}
                            body={auto.body}
                            drive_unit={auto.drive_unit}
                            fuel_type={auto.fuel_type}
                            transmission={auto.transmission}
                            power={auto.power}
                            volume_engine={auto.volume_engine}
                            fuel_volume={auto.fuel_volume}
                            acceleration_to100={auto.acceleration_to100}
                            seats_number={auto.seats_number}
                            city={auto.city}
                            rent_cost_per_day={auto.rent_cost_per_day}
                            rent_cost_per_month={auto.rent_cost_per_month}
                            description={auto.description}
                            links={auto.links}
                            id={auto.id}
                            imageUrl={auto.imageUrl}
                            onAboutClick={handleProductButtonClick}
                        />
                    ))}
                </div>
                {autosSize !== autos.length ? (
                    <button className={s.loadMoreBtn + " needAnimation"} onClick={loadMoreAutos}>Загрузить еще</button>
                ) : (
                    ""
                )}
            </div>

            <Popup trigger={selectedProduct} onClose={onClose}>
                <ExtendedCard {...getProductById(selectedProduct)}/>
            </Popup>
        </>

    )
}

export default Auto;
