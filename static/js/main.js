const getRoadId = (e) => e.id.split('-').at(-1)

const getDataById = (id) => ({
    point_0_id: +document.getElementById('road-start-point-id-' + id).innerText,
    point_1_id: +document.getElementById('road-end-point-id-' + id).innerText
})

const editRoadData = async (e) => {
    const id = getRoadId(e)
    const data = getDataById(id)
    debugger
    let response = await fetch('/roads/' + id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    })
    window.location.reload()
}

const deleteRoad = async (e) => {
    const id = getRoadId(e)
    debugger
    let response = await fetch('/roads/' + id, {
        method: 'DELETE'
    })
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
