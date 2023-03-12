const getId = (e) => e.id.split('-').at(-1)

const getRoadDataById = (id) => ({
    point_0_id: +document.getElementById('road-start-point-id-' + id).innerText,
    point_1_id: +document.getElementById('road-end-point-id-' + id).innerText
})

const postFetch = async (url, data) => {
    return await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    })
}

const putFetch = async (url, data) => {
    return await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    })
}

const deleteFetch = async (url) => {
    return await fetch(url, {
        method: 'DELETE'
    })
}

const editRoadData = async (e) => {
    const id = getId(e)
    const data = getRoadDataById(id)
    await putFetch('/roads/' + id, data)
    window.location.reload()
}

const deleteRoad = async (e) => {
    const id = getId(e)
    await deleteFetch('/roads/' + id)
    window.location.reload()
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
