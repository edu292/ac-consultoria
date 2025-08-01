function createPopupContent(data, lat, lng) {
    return `
        <p><strong>Endereço:</strong> ${data.logradouro || ''}, ${data.numero || ''} - ${data.bairro || ''}, ${data.cidade || ''}</p>
        <p>
            <strong>Latitude:</strong>
            <span>${lat}</span>
        </p>
        <p>
            <strong>Longitude:</strong>
            <span>${lng}</span>
        </p>
        <div class="coord-form">
            <label>
                <input id="coord-input-${data.id}" type="text">
            </label>
            <button id="save-btn-${data.id}">Salvar Coordenadas</button>
        </div>
    `;
}


async function patchMarkerLocation(id, lat, lng) {
    const factor = 10 ** 6;

    const truncatedLat = Math.trunc(lat * factor) / factor;
    const truncatedLng = Math.trunc(lng * factor) / factor;

    const newLocation = {
        latitude: truncatedLat,
        longitude: truncatedLng
    }

    const url = `/api/furtos/${id}`

    const response = await fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(newLocation)
    });
}


const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const map = L.map('map', {
    zoom: 7,
    center: [-24.61, -51.32],
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const locationData = JSON.parse(document.getElementById('locations-data').text)

const markers = locationData.forEach(data => {
    const marker = L.marker([data.latitude, data.longitude], {
        draggable: true
    })

    marker.db_id = data.id

    const popup = L.popup({
        content: createPopupContent(data, data.latitude, data.longitude)
    });

    marker.bindPopup(popup);
    marker.addTo(map);

    marker.on('dragend', async (event) => {
        const newPos = event.target.getLatLng();
        const success = patchMarkerLocation(marker.db_id, newPos.lat, newPos.lng)

        marker.setPopupContent(createPopupContent(data, newPos.lat, newPos.lng))
    });

    marker.on('popupopen', () => {
        const saveBtn = document.getElementById(`save-btn-${marker.db_id}`);
        saveBtn.addEventListener('click', async () => {
            const newPos = document.getElementById(`coord-input-${marker.db_id}`).value;
            let [newLat, newLng] = newPos.split(',').map(parseFloat)

            if (isNaN(newLat) || isNaN(newLng)) {
                alert('Por favor, insira valores numéricos válidos para latitude e longitude.');
                return;
            }

            const success = patchMarkerLocation(marker.db_id, newLat, newLng)

            marker.setLatLng([newLat, newLng]);
            const statusDiv = document.getElementById(`status-msg-${marker.db_id}`);
            if (statusDiv) {
                statusDiv.textContent = success ? 'Coordenadas salvas!' : 'Erro ao salvar!';
                statusDiv.className = success ? 'status-message success' : 'status-message error';
            }
        });
    });
});