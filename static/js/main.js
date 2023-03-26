/**
 * @param {HTMLElement} formElement
 * @returns object
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
 * @returns object
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
 * @returns Promise<void>
 */
const postRequest = async (formElement, url) => {
    const data = getFormData(formElement)
    await sendRequest(url, 'POST', data)
    window.location.reload()
}


/**
 * @param {HTMLElement} tableRowElement
 * @param {string} url
 * @returns Promise<void>
 */
const putRequest = async (tableRowElement, url) => {
    const data = getTableRowData(tableRowElement)
    await sendRequest(url, 'PUT', data)
    window.location.reload()
}


/**
 * @param {string} url
 * @returns Promise<void>
 */
const deleteRequest = async (url) => {
    await sendRequest(url, 'DELETE')
    window.location.reload()
}


/**
 * @param {string} url
 * @param {string} method
 * @param {object | null} data
 * @returns Promise<Response>
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

/**
 * @param {string} elementId
 * @returns {number}
 */
const getSelectedId = (elementId) => {
    const element = document.getElementById(elementId)
    return +element
        .options[element.selectedIndex]
        .id
        .split('-')
        .at(-1)
}

/**
 * @returns {Promise<void>}
 */
const getCityPlaces = async () => {
    const cityId = getSelectedId('cities')
    const cityPlaces = await fetch('/places?city_id=' + cityId)
        .then(r => r.json())
        .then(r => r.data)

    document.getElementById('accommodation').innerHTML = cityPlaces
        .map(place => mapPlaceObjectToOption(place, 'accommodation').outerHTML)
        .join('')

    document.getElementById('visit').innerHTML = cityPlaces
        .map(place => mapPlaceObjectToOption(place, 'visit').outerHTML)
        .join('')
}

/**
 * @param {HTMLOptionElement} option
 * @returns {{id: number, name: string, address: string}}
 */
const mapPlaceOptionToObject = option => ({
    id: +option.value,
    name: option.getAttribute('data-name'),
    address: option.getAttribute('data-address')
})

/**
 * @param {object: {id: number, name: string, address: string}} data
 * @param {string} prefix
 * @returns {HTMLOptionElement}
 */
const mapPlaceObjectToOption = (data, prefix = 'place') => {
    const option = new Option(`${data.name} (${data.address})`, `${data.id}`)
    option.id = `${prefix}-${data.id}`
    option.setAttribute('data-name', data.name)
    option.setAttribute('data-address', data.address)
    return option
}

/**
 * @returns {{place_id: number, stay_time: string, date: string, time: string, priority: boolean}[]}
 */
const getVisits = () => {
    return [
        ...document
            .getElementById('visits-table-body')
            .getElementsByTagName('tr')
    ]
        .filter(tr => tr.getElementsByTagName('td').length > 0)
        .map(visitRow => {
            const inputs = [...visitRow.getElementsByTagName('input')]
            return {
                place_id: +inputs
                    .filter(input => input.name === 'place_id')
                    .map(input => input.value)
                    .at(0),
                stay_time: inputs
                    .filter(input => input.name === 'stay_time')
                    .map(input => input.value)
                    .at(0),
                date: inputs
                    .filter(input => input.name === 'date')
                    .map(input => input.value ? new Date(input.value).toLocaleDateString() : input.value)
                    .at(0),
                time: inputs
                    .filter(input => input.name === 'time')
                    .map(input => input.value)
                    .at(0),
                priority: inputs
                    .filter(input => input.name === 'priority')
                    .map(input => input.checked)
                    .at(0)
            }
        })
}

/**
 * @param {HTMLSelectElement} select
 * @returns {{id: number, name: string, address: string}}
 */
const getSelectedPlace = select => {
    return [...select.getElementsByTagName('option')]
        .filter(option => option.selected)
        .map(option => mapPlaceOptionToObject(option))
        .at(0)
}

/**
 * @returns void
 */
const addVisit = () => {
    const place = getSelectedPlace(document.getElementById('visit'))
    const tableBody = document.getElementById('visits-table-body')

    if (tableBody.children.length === 0) {
        document
            .getElementById('visits-table-caption')
            .removeAttribute('hidden')
        tableBody.innerHTML = `
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
    }

    tableBody.innerHTML += `
        <tr class="py-4">
            <td class="border-r" hidden>
                <input name="place_id" value="${place.id}" hidden>
            </td>
            <td class="border-r">${place.name}</td>
            <td class="border-r">${place.address}</td>
            <td class="border-r">
                <input class="focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none text-sm leading-6
                              text-slate-900 placeholder-slate-400 rounded-md py-2 pl-4 ring-1 ring-slate-200 shadow-sm
                              grow shrink basis-33-minus-1rem"
                       name="stay_time"
                       type="time"
                       min="00:00"
                       max="23:59"
                       required>
            </td>
            <td class="border-r">
                <input class="focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none text-sm leading-6
                              text-slate-900 placeholder-slate-400 rounded-md py-2 pl-4 ring-1 ring-slate-200 shadow-sm
                              grow shrink basis-33-minus-1rem"
                       name="date"
                       type="date">
            </td>
            <td class="border-r">
                <input class="focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none text-sm leading-6
                              text-slate-900 placeholder-slate-400 rounded-md py-2 pl-4 ring-1 ring-slate-200 shadow-sm
                              grow shrink basis-33-minus-1rem"
                       name="time"
                       type="time"
                       min="00:00"
                       max="23:59">
            </td>
            <td class="border-r">
                <input class="focus:ring-2 focus:ring-blue-500 focus:outline-none appearance-none text-sm leading-6
                              text-slate-900 placeholder-slate-400 rounded-md py-2 pl-4 ring-1 ring-slate-200 shadow-sm
                              grow shrink basis-33-minus-1rem"
                       name="priority"
                       type="checkbox"
                       checked>
            </td>
            <td>
                <button class="px-6 py-2 bg-red-500 rounded-md text-white"
                        onclick="deleteVisit(this.parentElement.parentElement)">X
                </button>
            </td>
        </tr>
    `
}

/**
 * @param {HTMLTableRowElement} visit
 */
const deleteVisit = visit => {
    const tableBody = document.getElementById('visits-table-body')

    if (tableBody.children.length <= 2) {
        clearVisitsTable()
    } else {
        tableBody.removeChild(visit)
    }
}

const clearVisitsTable = () => {
    document
        .getElementById('visits-table-caption')
        .setAttribute('hidden', '')
    document
        .getElementById('visits-table-body')
        .innerHTML = ''
}

const getRoutes = async (secret) => {
    let cityId = getSelectedId('cities')

    if (cityId) {
        const visits = getVisits()
        const startsAt = document.getElementById('starts-at').value
        const endsAt = document.getElementById('ends-at').value
        const accommodation = getSelectedPlace(document.getElementById('accommodation'))

        await fetch('/trips/' + secret, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                city_id: cityId,
                accommodation_id: accommodation ? accommodation.id : '',
                starts_at: startsAt ? new Date(startsAt).toLocaleDateString() : startsAt,
                ends_at: endsAt ? new Date(endsAt).toLocaleDateString() : endsAt,
                awakens_at: document.getElementById('awakens-at').value,
                rests_at: document.getElementById('rests-at').value,
                visits: visits
            })
        })
    }

    window.location = `/trips/${secret}/routes`
}

const citySelect = document.getElementById('cities')
const accommodationSelect = document.getElementById('accommodation')
const magnifyingArea = document.getElementById('magnifying-area')
const magnifyingImage = document.getElementById('magnifying-image')
const scale = 4
const scaling = (scale - 1) * 105
const offset = scaling / 2

if (citySelect) {
    citySelect.addEventListener('change', async () => {
        await getCityPlaces()
        clearVisitsTable()
    })
    if (accommodationSelect?.children?.length === 0) {
        getCityPlaces().then()
    }
}

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
