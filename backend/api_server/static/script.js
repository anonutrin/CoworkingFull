const tg = window.Telegram.WebApp;


const CHUNK_SIZE = 50;
let currentChunk = 0;
let isLoading = false;
let locations = [];
const $map = document.querySelector('#map');

function expandTelegram() {
    tg.expand();
}

function showBackButton() {
    if (window.Telegram && window.Telegram.WebApp) {
        Telegram.WebApp.BackButton.show();
        Telegram.WebApp.BackButton.onClick(() => {
            window.history.back();
        });
    }
}

function parseUrlSearchParams() {
    const urlSearchParams = new URLSearchParams(window.location.search);
    return Object.fromEntries(urlSearchParams.entries());
}

function getDefaultCoordinates() {
    return [55.76, 37.64];
}

function sendTelegramData(data) {
    try {
        tg.sendData(data);
    } catch (error) {
        console.error(error);
    }
}

function getLocationChunk(currentChunk, chunkSize) {
    const start = currentChunk * chunkSize;
    const end = start + chunkSize;
    return locations.slice(start, end);
}

function getLocationIdFromUrl() {
    const url = window.location.href;
    const parts = url.split('/');
    const idIndex = parts.indexOf('location') + 1;
    if (idIndex > 0 && idIndex < parts.length) {
        return parts[idIndex];
    }
    return null;
}

function setActiveJobTypeBtn(enabledElement) {
    document.querySelectorAll('.button-job-type').forEach(btn => {
        btn.classList.remove('active');
    });
    enabledElement.classList.add('active');
}

async function fetchLocations(sphere, price) {
    const uriComponent = `sphere=${sphere}&priceTo=${price}`;
    const url = `https://masterlocation.ru:8099/locations?${uriComponent}`;

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}

async function loadMapPoints(activeLocationId = null) {
    if (isLoading) return;

    isLoading = true;

    try {
        const data = getLocationChunk(currentChunk, CHUNK_SIZE);

        if (!data.length) {
            isLoading = false;
            return;
        }

        data.forEach(item => {
            try {
                const catEmodji = item.emodji || '';
                const itemContent = `${catEmodji}${(item?.price?.match(/[\d\.]+/) || '')}`;

                const placemark = new ymaps.Placemark(
                    [item.latitude, item.longitude],
                    {
                        iconContent: itemContent,
                        hintContent: item.title,
                        balloonContentHeader: `
                            <div class="desc-header">
                                <div class="header-title">
                                    <a href="?show_hotel='${item.id}'">${item.title}</a>
                                </div>
                                <div class="header-info">
                                    <span class="description">
                                        <span class="desc-rating">${item.price}</span>
                                    </span>
                                </div>
                            </div>
                        `,
                        balloonContentBody: `
                          <div class="desc-block" style="max-height: 300px" xmlns="http://www.w3.org/1999/html">
                            <div class="img-block">
                              <a style="width:100%;height:100%" href="?show_hotel='${item.id}'"><img src="image/${item.id}" alt=""/></a>
                            </div>
                            <div class="desc-text">
                              <div class="text-apart" style="display: flex; flex-direction: column; height: 100%">
                                <div class="text-content" style="flex: 1 1 auto;">
                                  ${item?.short_description?.split('\n').reduce((store, el) => store + `<div><span>${el}</span></div>`, '')}
                                  <div>
                                    <span class="work-schedule">${item.work_schedule || ""}</span>
                                    </div>
                                            </div>
                                            <div style="
                                                padding: 5px 0;
                                                margin-top: 10px;
                                                border-radius: 5px;
                                                background-color: #0044bb;
                                                color: whitesmoke;
                                                width: 100%;
                                                text-align: center;
                                            ">
                                                <button class="choose-btn" data-locid="${item.id}">Выбрать</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                        `
                    },
                    {
                        preset: "islands#violetStretchyIcon",
                        balloonPanelMaxMapArea: Infinity,
                        balloonMaxHeight: 200
                    }
                );
                myMap.geoObjects.add(placemark);
                if (+activeLocationId === item.id)
                    placemark.balloon.open();

            } catch (error) {
                console.error(error);
            }
        });

        currentChunk++;
        isLoading = false;

        setTimeout(loadMapPoints, 0);
    } catch (error) {
        isLoading = false;
        console.error(error);
    }
}

function initializeMap(coordinates = null) {
    try {
        myMap = new ymaps.Map("map", {
            center: coordinates || getDefaultCoordinates(),
            zoom: 9,
            controls: [
                new ymaps.control.SearchControl({
                    options: {
                        provider: 'yandex#search'
                    }
                })
            ]
        });
    } catch (error) {
        console.error(error);
    }
}

function initializeFilters() {
    let sphere = '';
    try {
        const filterBtn = document.querySelector('.filter-btn');
        const rangePriceValue = document.querySelector('.price-value');
        const priceRange = document.querySelector('#price-range');
        const filterButtons = document.querySelector('.filter-buttons');
        const submitFilter = document.querySelector('.submit-button');
        const filterWrapper = document.querySelector('.filter-wrapper');
        const closeFilterBtn = document.querySelector('#close-filter-btn');

        filterWrapper.style.display = 'none';
        filterBtn.style.display = 'flex';

        filterBtn.addEventListener('click', () => {
            console.log(filterWrapper.style.display);
            if (filterWrapper.style.display === 'none') {
                filterWrapper.style.display = 'block';
            } else {
                filterWrapper.style.display = 'none';
            }
        });
        filterButtons.addEventListener('click', (e) => {
            const jobtype = e.target.dataset.jobtype;
            if (jobtype) {
                setActiveJobTypeBtn(e.target);
                sphere = jobtype;
            }
        });
        priceRange.addEventListener('change', (e) => {
            priceTo = parseFloat(e.target.value);
            rangePriceValue.textContent = e.target.value + '₽';
        });
        submitFilter.addEventListener('click', async (e) => {
            myMap.geoObjects.removeAll();
            currentChunk = 0;
            locations = await fetchLocations(sphere, priceRange.value);
            await loadMapPoints();
            filterWrapper.style.display = 'none';
        });
        closeFilterBtn.addEventListener('click', () => {
            filterWrapper.style.display = 'none';
        });

    } catch (error) {
        console.error(error);
    }
}

function initUserInterface(mapContainer) {
    mapContainer.insertAdjacentHTML('beforeend', `
    <div id="sett-btns" style="position: absolute; top: 45px; left: 10px; z-index: 1;">
        <button class="filter-btn" style="display: none">
          <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAABvElEQVR4nO2aL0hDURSHv02mDFkaCApDDBaDxWISBAUxmWw224LBYlCwLtpsgsEiJpPJMA0ymyIiBoNBEAR1iuKfKw/O4CHq7ra3986V+8Fr55z7OzvvnXfu3QOPbsqAceQq/5WIcez6lboGSjC2ieTRS94mkWMxOAJy6CMn2gKNJ38Z9gDnYngAdKOHLLAv2i6BvnoOBeBKHPaALpInA+yKpmtgwNZxELgRxx2gg+RIA1ui5RYYajTAMHAnATaAFPGTAtZFwz0w0mygUeBRAq0RPyVZ+xkYazXYBPAiAZeJjxVZ8xWYjiroDPAmgRdpP0VZ6x2YjTr4HPABfALzUQePe51iO38pYq58W+7dpJ7FUpTdJMnumIqqv2t4X6VbfeNqmiAyzc5AGme67LeptNfCR+2UnQvtEyoW9hXN+558A1tl9TtR02AiajE+EWUYXxFlGF8RZRhfEWUYXxFlGF8RZRhfEWWY/1aRSUs7tRyGRG7LAYOTiWSABeBBhD4Bqz+ckKhPpEbw/95mSPAFMOViIjXGgdOQ8OAMrN/FRAI6gSWgKuKrriZSoyANwOoTDBcIWvNZvY9iPDjOF32YJjhd5JEGAAAAAElFTkSuQmCC">
          <span>Фильтр</span>
        </button>
    </div>
  `);
    mapContainer.insertAdjacentHTML('beforeend', `
    <div class="filter-wrapper" style="display: none">
          <span id="close-filter-btn" style="
            position: absolute;
            top: 15px;
            right: 10px;
            cursor: pointer;
            font-size: 30px;
        ">X</span>

        <div class="block-filter" >
            <h1>Рабочее место</h1>
            <div class="filter-buttons">
                <div class="button-row">
                    <button data-jobtype="визажист" class="button-job-type">Для визажиста</button>
                    <button data-jobtype="парикмахер" class="button-job-type">Для парикмахера</button>
                </div>
                <div class="button-row">
                    <button data-jobtype="колорист" class="button-job-type">Для колориста</button>
                    <button data-jobtype="маникюр" class="button-job-type">Для мастера маникюру</button>
                </div>
                <div class="button-row">
                    <button data-jobtype="все" class="button-job-type active">Для всех</button>
                </div>
            </div>
            <div class="price-range">
                <label for="price-range">Ценовой диапазон до:</label>
                <input type="range" id="price-range" name="price-range" min="0" max="100000" value="100000"></br>
                <span class="price-value">100000₽</span>
            </div>
            <button class="submit-button">Изменить</button>
        </div>
      </div>
  `);
}

$map.addEventListener('click', async e => {
    if (e.target.classList.contains('choose-btn')) {
        prompt('', tg.initDataUnsafe);
        await fetchShowLocation(tg.initDataUnsafe?.user?.id, e.target.dataset.locid);
        tg.close();
    }
})


async function fetchShowLocation(chat_id, location_id) {
    const data = new URLSearchParams();
    if (chat_id)
        data.append('chat_id', chat_id);
    if (location_id)
        data.append('location_id', location_id);

    const url = `http://localhost:5001/show?${data.toString()}`;

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}

async function fetchUserInfo(chat_id) {
    const data = new URLSearchParams();
    if (chat_id)
        data.append('chat_id', chat_id);

    const url = `http://localhost:5001/user-info?${data.toString()}`;

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
        return {};
    }
}

async function main() {
    expandTelegram();
    showBackButton();
    const params = parseUrlSearchParams();

    const user = tg.initDataUnsafe.user;
    user_info = await fetchUserInfo(user?.id);
    const coordinates = user_info?.latitude && user_info?.longitude ? [params.latitude, params.longitude] : getDefaultCoordinates();

    let {sphere = '', priceTo = ''} = params;
    let activeLocationId = null;

    if (Object.entries(params).length) {
        if ('show_hotel' in params)
            sendTelegramData(params.show_hotel);
        if ('location' in params) {
            sphere = '';
            priceTo = '';
            activeLocationId = params.location;
        }
    }

    const mapContainer = document.querySelector('#map');
    initUserInterface(mapContainer);

    let myMap;

    ymaps.ready(() => {
        initializeMap(coordinates);

        fetchLocations(sphere, priceTo).then(async data => {
            locations = data;
            await loadMapPoints(activeLocationId);
            initializeFilters();
        });


    });
}

(async function () {
    await main();
}());
