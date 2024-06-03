import React, {useEffect, useState} from "react";
import s from './Location.module.css';
import LocationCard from "./LocationCard/LocationCard";
import {useTelegram} from "../../hooks/useTelegram";
import Popup from "../Popup/Popup";
import {fetchLocations} from "../../api/api";
import ExtendedLocationCard from "./ExtendedLocationCard/ExtendedLocationCard";
import {IoFilterSharp} from "react-icons/io5";


const Location = () => {
    const [locations, setLocations] = useState([]);
    const [locationSize, setLocationSize] = useState(0);
    const [selectedProduct, setSelectedProduct] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);

    const {showBackButton, toMain} = useTelegram();

    const [showFilter, setShowFilter] = useState(false);
    const [maxPrice, setMaxPrice] = useState(0);

    const [selectedCategory, setSelectedCategory] = useState('Все');
    const [tempSelectedCategory, setTempSelectedCategory] = useState('Все');
    const [tempMaxPrice, setTempMaxPrice] = useState(0);

    useEffect(() => {
        showBackButton(toMain);
    }, []);

    const loadLocations = async () => {
            try {
                console.log(currentPage, maxPrice, selectedCategory);
                const {data, totalLocations} = await fetchLocations(currentPage, maxPrice, selectedCategory);
                setLocationSize(totalLocations);
                setLocations((prevLocations) => {
                    const newData = data.filter(newLocation => !prevLocations.some(prevLocation => prevLocation.id === newLocation.id));
                    return [...prevLocations, ...newData];
                });
            } catch (error) {
                console.error("Error fetching locations:", error);
            }
        };

    useEffect(() => {
        loadLocations();

    }, [currentPage]);

    const handleProductButtonClick = (event) => {
        const productId = event.target.dataset.id;
        setSelectedProduct(productId);
    };

    const onClose = () => {
        setSelectedProduct(null);
    };
    const onCloseFilter = () => {
        setShowFilter(false);
    };

    const getProductById = (productId) => {
        return locations.find((product) => {
            return product.id === +productId;
        }) || {};
    };

    const loadMoreLocations = () => {
        setCurrentPage((prevPage) => prevPage + 1);
    };

    const toggleFilterActive = () => {
        setShowFilter(!showFilter);
    }
    const handleMaxPriceChange = (event) => {
        setTempMaxPrice(event.target.value);
    };

    const handleCategoryChange = (event) => {
        setTempSelectedCategory(event.target.value);
    };

    const handleSaveButtonClick = () => {
        setMaxPrice(tempMaxPrice);
        setSelectedCategory(tempSelectedCategory);
        setLocationSize(0);
        setLocations([]);
        setShowFilter(false);
        if(currentPage !== 1) {
            setCurrentPage(1);
        } else {
            setCurrentPage(0);
        }

    };

    return (
        <>

            <div className={s.locationBlock}>
                <div className={s.filtAndTitle}>
                    {
                        <div className={s.mainTitle}>Поможем подобрать локации</div>
                    }
                    <a className={s.filterBtn + " needAnimation"} onClick={toggleFilterActive}>
                        Фильтр <IoFilterSharp size="25"/>
                    </a>
                </div>

                <div className={s.cardsBlock}>
                    {locations.map((location) => (
                        <LocationCard
                            key={location.id}
                            id={location.id}
                            title={location.title}
                            imageUrl={location.imageUrl}
                            full_address={location.full_address}
                            short_description={location.short_description}
                            price={location.price}
                            contact_link={location.contact_link}
                            work_schedule={location.work_schedule}
                            category={location.category}
                            onAboutClick={handleProductButtonClick}
                        />
                    ))}
                </div>
                {locationSize !== locations.length ? (
                    <button className={s.loadMoreBtn + " needAnimation"} onClick={loadMoreLocations}>Загрузить еще</button>
                ) : (
                    ""
                )}
            </div>
            <Popup trigger={selectedProduct} onClose={onClose}>
                <ExtendedLocationCard {...getProductById(selectedProduct)}/>
            </Popup>
            <Popup trigger={showFilter} onClose={onCloseFilter}>
                <div className={s.filterBlock}>
                    <div className={s.filterCat}>
                        <label htmlFor="categories">Категория:</label>
                        <select id={"categories"} value={tempSelectedCategory} onChange={handleCategoryChange}>
                            <option value={"Все"}>Все</option>
                            <option value={"Колорист"}>Колорист</option>
                            <option value={"Визажист"}>Визажист</option>
                            <option value={"Парикмахер"}>Парикмахер</option>
                            <option value={"Маникюр"}>Маникюр</option>
                        </select>
                    </div>
                    <div className={s.filterPrice}>
                        <label htmlFor="max_price">Цена до:</label>
                        <input type={"number"} step="10" min="100" value={tempMaxPrice} onChange={handleMaxPriceChange}/>
                    </div>
                    <button onClick={handleSaveButtonClick}>Сохранить</button>
                </div>
            </Popup>
            <div className={s.mapBtn + " needAnimation"}>
                <a href="/map">На карте</a>
            </div>
        </>
    );
}

export default Location;
