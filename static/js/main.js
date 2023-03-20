/**
 * @param {HTMLElement} formElement
 * @returns {object}
 */
const getFormData = (formElement) => {
    const data = {};
    for (const inputElement of formElement.getElementsByTagName('input')) {
        data[inputElement.name] = inputElement.value
    }
    return data
}

/**
 * @param {HTMLElement} tableRowElement
 * @returns {object}
 */
const getTableRowData = (tableRowElement) => {
    const data = {};
    for (const tdElement of tableRowElement.getElementsByTagName('td')) {
        if (tdElement.title) {
            data[tdElement.title] = tdElement.innerText
        }
    }
    return data
}


/**
 * @param {HTMLElement} formElement
 * @param {string} url
 * @returns {Promise<void>}
 */
const postRequest = async (formElement, url) => {
    const data = getFormData(formElement)
    await sendRequest(url, 'POST', data)
    window.location.reload()
}


/**
 * @param {HTMLElement} tableRowElement
 * @param {string} url
 * @returns {Promise<void>}
 */
const putRequest = async (tableRowElement, url) => {
    const data = getTableRowData(tableRowElement)
    await sendRequest(url, 'PUT', data)
    window.location.reload()
}


/**
 * @param {string} url
 * @returns {Promise<void>}
 */
const deleteRequest = async (url) => {
    await sendRequest(url, 'DELETE')
    window.location.reload()
}


/**
 * @param {string} url
 * @param {string} method
 * @param {object | null} data
 * @returns {Promise<Response>}
 */
const sendRequest = async (url, method, data = null) => {
    const request = {
        method: method
    }

    if (data) {
        request.headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        request.body = JSON.stringify(data)
    }

    return await fetch(url, request)
}

const getSelectedId = (elementId) => {
    let element = document.getElementById(elementId)
    return +element
        .options[element.selectedIndex]
        .id
        .split('-')
        .at(-1)
}

let cityPlaces = []
let cityId = 0

const getCityPlaces = async () => {
    let citiesElement = document.getElementById('places')
    let stayPlaceElement = document.getElementById('stay-place')
    cityId = getSelectedId('cities')
    cityPlaces = await fetch('/places/?city_id=' + cityId)
        .then(r => r.json())
        .then(r => r.data)

    if (cityId > 0) {
        let button = document.getElementById('send-data')
        button.classList.add('bg-green-500')
        button.classList.remove('bg-gray-500')
    } else {
        let button = document.getElementById('send-data')
        button.classList.add('bg-gray-500')
        button.classList.remove('bg-green-500')
    }

    stayPlaceElement.innerHTML = ''
    cityPlaces.forEach(place => stayPlaceElement.innerHTML +=
        `<option id="place-${place.id}">${place.name} (${place.address})</option>`)

    citiesElement.innerHTML = ''
    cityPlaces.forEach(place => citiesElement.innerHTML +=
        `<option id="place-${place.id}">${place.name} (${place.address})</option>`)
}

const selectedPlaces = []

const addCityPlace = () => {
    const selectedId = getSelectedId('places')
    selectedPlaces.unshift(cityPlaces.find(place => place.id === selectedId))
    let addedPlacesElement = document.getElementById('addedPlaces')

    addedPlacesElement.innerHTML =
        `
        <caption class="text-xl font-medium p-2" style="text-align: left">Выбранные места</caption>
        <tr class="border-b">
            <th class="border-r">Название</th>
            <th class="border-r">Адрес</th>
            <th class="border-r">Длительность</th>
            <th class="border-r">Дата</th>
            <th class="border-r">Время</th>
            <th class="border-r">Обязательно</th>
            <th class=""></th>
        </tr>
        `

    selectedPlaces.forEach((place, index) => addedPlacesElement.innerHTML +=
        `
        <tr class="py-4">
            <td class="border-r">${place.name}</td>
            <td class="border-r">${place.address}</td>
            <td class="border-r">
                <input class="focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none text-sm leading-6
                              text-slate-900 placeholder-slate-400 rounded-md py-2 pl-4 ring-1 ring-slate-200 shadow-sm
                              grow shrink basis-33-minus-1rem" 
                          type="time" 
                          min="00:01" 
                          max="23:59" 
                          required
                          id="stay-time-${index}">
            </td>
            <td class="border-r">
                <input class="focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none text-sm leading-6
                              text-slate-900 placeholder-slate-400 rounded-md py-2 pl-4 ring-1 ring-slate-200 shadow-sm
                              grow shrink basis-33-minus-1rem" 
                          type="date" 
                          required
                          id="date-${index}">
            </td>
            <td class="border-r">
                <input class="focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none text-sm leading-6
                              text-slate-900 placeholder-slate-400 rounded-md py-2 pl-4 ring-1 ring-slate-200 shadow-sm
                              grow shrink basis-33-minus-1rem" 
                          type="time"
                          min="00:01" 
                          max="23:59"
                          required
                          id="time-${index}">
            </td>
            <td class="border-r">
                <input class="focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none text-sm leading-6
                              text-slate-900 placeholder-slate-400 rounded-md py-2 pl-4 ring-1 ring-slate-200 shadow-sm
                              grow shrink basis-33-minus-1rem" 
                              type="checkbox" 
                              checked 
                              required
                              id="priority-${index}">
            </td>
            <td>
                <button class="px-6 py-2 bg-red-500 rounded-md text-white"
                        id=""
                        onclick="">X
                </button>
            </td>
        </tr>
        `
    )
}

const routeBuilt = async (secret) => {
    if (cityId !== 0) {
        let places = selectedPlaces.map((place, index) => {
            return {
                place_id: place.id,
                stay_time: document.getElementById('stay-time-' + index).value,
                date: new Date(document.getElementById('date-' + index).value).toLocaleDateString(),
                time: document.getElementById('time-' + index).value,
                priority: document.getElementById('priority-' + index).checked
            }
        })

        let data = {
            city_id: cityId,
            accommodation_id: +document.getElementById('stay-place')
                .options[document.getElementById('stay-place').selectedIndex]
                .id.split('-').at(-1),
            starts_at: new Date(document.getElementById('starts-at').value).toLocaleDateString(),
            ends_at: new Date(document.getElementById('ends-at').value).toLocaleDateString(),
            awakens_at: document.getElementById('awakens-at').value,
            rests_at: document.getElementById('rests-at').value,
            visits: places
        }

        await fetch('/trips/' + secret, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        window.location = `/trips/${secret}/routes`
    }
}

const magnifyingArea = document.getElementById('magnifying-area')
const magnifyingImage = document.getElementById('magnifying-image')
const scale = 4
const scaling = (scale - 1) * 105
const offset = scaling / 2

magnifyingArea?.addEventListener('mousemove', event => {
    let clientX = event.clientX - (window.innerWidth - magnifyingArea.offsetWidth) / 2
    let clientY = event.clientY - (window.innerHeight - magnifyingArea.offsetHeight) / 2

    clientX = -clientX / magnifyingArea.offsetWidth * scaling + offset
    clientY = -clientY / magnifyingArea.offsetHeight * scaling + offset

    magnifyingImage.style.transform = `translate(${clientX}%, ${clientY}%) scale(${scale})`
})

magnifyingArea?.addEventListener('mouseleave', () => {
    magnifyingImage.style.transform = 'translate(0%, 0%) scale(1)'
})
