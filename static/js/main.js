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
