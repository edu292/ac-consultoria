var map = L.map('map', {
    zoom: 7,
    center: [-24.61, -51.32],
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const geojsonUrl = 'https://raw.githubusercontent.com/giuliano-macedo/geodata-br-states/refs/heads/main/geojson/br_states/br_pr.json';

fetch(geojsonUrl)
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            style: {
                "color": "#007bff",
                "weight": 3,
                "opacity": 0.8
            },
        }).addTo(map);
    })
    .catch(error => console.error('Error loading the GeoJSON data:', error));

L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
    initialize: function(index, options) {
        var playerOptions = {
            buffer: 1,
            minBufferReady: -1
            };
        options.playerOptions = { ...playerOptions, ...(options.playerOptions || {}) };
        L.Control.TimeDimension.prototype.initialize.call(this, options);
        this.index = index;
    },
    _getDisplayDateFormat: function(date) {
        return this.index[date-1];
    }
});

const timeLabels = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', 'Total']
const times = Array.from({ length: timeLabels.length }, (_, i) => i+1);

map.timeDimension = L.timeDimension(
    {times : times, currentTime: new Date(1)}
);

var timeDimension = new L.Control.TimeDimensionCustom(timeLabels, {
    autoPlay: false,
    backwardButton: true,
    displayDate: true,
    forwardButton: true,
    limitMinimumRange: 5,
    limitSliders: true,
    loopButton: false,
    maxSpeed: 10,
    minSpeed: 0.1,
    playButton: false,
    playReverseButton: false,
    position: "bottomleft",
    speedSlider: false,
    speedStep: 0.1,
    styleNS: "leaflet-control-timecontrol",
    timeSlider: true,
    timeSliderDragUpdate: false,
    timeSteps: 1
}).addTo(map);

const heatmapLayer = new HeatmapOverlay({
    radius: 15,
    blur: 0.8,
    maxOpacity: 0.6,
    scaleRadius: false,
    useLocalExtrema: false,
    latField: 'lat',
    lngField: 'lng',
    valueField: 'count',
    defaultWeight : 1,
}).addTo(map);

const cluster = L.markerClusterGroup().addTo(map);

const tooltip = new L.Tooltip().setContent('Clique para ver mais informações');

const baseURL = 'api/geoloc/?month='

class LazyLocationData {
  constructor(length) {
    this.length = length;
    this._rawCache = new Map();
    this._transformedCache = new Map();
  }

  async _getRawData(index) {
    if (this._rawCache.has(index)) {
      return this._rawCache.get(index);
    }

    let dataPromise;
    if (index === this.length) {
      const allPromises = Array.from({ length: this.length-1 }, (_, i) => this._getRawData(i+1));
      dataPromise = Promise.all(allPromises).then(allData => allData.flat());
    } else {
      dataPromise = fetch(baseURL+index).then(response => response.json());
    }

    this._rawCache.set(index, dataPromise);
    const data = await dataPromise;
    this._rawCache.set(index, data);
    return data;
  }


  async asMarkers(index) {
    if (this._transformedCache.get(index)?.has('markers')) {
      return this._transformedCache.get(index).get('markers');
    }

    const rawData = await this._getRawData(index);

    const markers = rawData.map(point => {
        return L.marker([point.latitude, point.longitude])
            .bindPopup(
                L.popup()
                    .setContent('Data: '+point.date+'<br>'+'Tipo de Equipamento: '+point.type)
            )
            .bindTooltip(tooltip)
    });

    if (!this._transformedCache.has(index)) {
      this._transformedCache.set(index, new Map());
    }
    this._transformedCache.get(index).set('markers', markers);

    return markers;
  }

  async asHeatmapArray(index) {
    if (this._transformedCache.get(index)?.has('heatmap')) {
      return this._transformedCache.get(index).get('heatmap');
    }

    const rawData = await this._getRawData(index);

    const heatmap = {
      data: rawData.map(p => ({ lat: p.latitude, lng: p.longitude, count: 1 }))
    };

    if (!this._transformedCache.has(index)) {
      this._transformedCache.set(index, new Map());
    }
    this._transformedCache.get(index).set('heatmap', heatmap);

    return heatmap;
  }
}

async function main() {

    let currentIndex = 0
    let markersByMonth = new LazyLocationData(8)

    map.timeDimension.on('timeload', async function (e) {
        let newIndex = e.time;
        if (newIndex === currentIndex) return;
        currentIndex = newIndex
        const [markers, heatmapArray] = await Promise.all([
            markersByMonth.asMarkers(newIndex),
            markersByMonth.asHeatmapArray(newIndex)
        ]);
        cluster.clearLayers();
        cluster.addLayers(markers);
        heatmapLayer.setData(heatmapArray);
    });
}
main()
map.timeDimension.fire('timeload', {time: 1});