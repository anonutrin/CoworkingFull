// const apiEndpoint = 'https://localhost:8099'
const apiEndpoint = 'https://allrenda.ru:8099'

async function fetchLocations(page, max_price=null, category=null) {
    try {
        const response = await fetch(`${apiEndpoint}/chunkLocations?page=${page}&max_price=${max_price}&category=${category}`);
        if (!response.ok) {
            console.log('Failed to fetch locations')
            return {data: [], totalLocations: 0}
        }
        const data = await response.json();
        return {data: data.locations, totalLocations: data.total_count}

    } catch (e) {
        console.log('Failed to fetch locations:', e);
        return {data: [], totalLocations: 0}
    }
}

async function fetchAutos(page) {
    try {
        const response = await fetch(`${apiEndpoint}/chunkAutos?page=${page}`);
        if (!response.ok) {
            console.log('Failed to fetch locations')
            return {data: [], totalAuto: 0}
        }
        const data = await response.json();
        return {data: data.autos, totalAuto: data.total_count}

    } catch (e) {
        console.log('Failed to fetch locations:', e);
        return {data: [], totalAuto: 0}
    }
}

export {fetchLocations, fetchAutos, apiEndpoint};