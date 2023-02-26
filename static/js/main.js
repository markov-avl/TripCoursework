const fetchPost = async (e) => {
    const idNumber = e.id.split('-').at(-1)
    const roadStartIdElement = document.getElementById('road-start-' + idNumber)
    const roadEndIdElement = document.getElementById('road-end-' + idNumber)

    const road = {
        id: +idNumber,
        point_0_id: +roadStartIdElement.innerText,
        point_1_id: +roadEndIdElement.innerText
    }

    let response = await fetch('url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(road)
    })

    let result = await response.json()
    window.location.reload()
}

const magnifyingArea = document.getElementById('magnifying-area')
const magnifyingImage = document.getElementById('magnifying-image')

magnifyingArea?.addEventListener('mousemove', event => {
    let clientX = event.clientX - (window.innerWidth - magnifyingArea.offsetWidth) / 2
    let clientY = event.clientY - (window.innerHeight - magnifyingArea.offsetHeight) / 2

    clientX = -clientX / magnifyingArea.offsetWidth * 100 + 50
    clientY = -clientY / magnifyingArea.offsetHeight * 100 + 50

    magnifyingImage.style.transform = `translate(${clientX}%, ${clientY}%) scale(2)`
})

magnifyingArea?.addEventListener('mouseleave', () => {
    magnifyingImage.style.transform = 'translate(0%, 0%) scale(1)'
})
