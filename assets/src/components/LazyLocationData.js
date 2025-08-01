export default class LazyLocationData {
    constructor(length) {
        this.length = length
        this._rawCache = new Map();
        this._transformedCache = new Map();
        this.ALL_DATA_KEY = 'all'
    }

    async _getRawData(index) {
        if (this._rawCache.has(index)) {
            return this._rawCache.get(index);
        }

        let dataPromise;
        const baseURL = 'api/furtos/?month=';
        if (index === this.ALL_DATA_KEY) {
          const allPromises = Array.from({ length: this.length }, (_, i) => this._getRawData(i+1));
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

        const tooltip = new L.Tooltip().setContent('Clique para ver mais informações');
        const rawData = await this._getRawData(index);

        const markers = rawData.map(point => {
            return L.marker([point.latitude, point.longitude])
                .bindPopup(
                    L.popup({
                        content: `Data: ${point.data_ocorrencia}<br>
                                 Tipo de Equipamento: ${point.tipo_de_equipamento}`
                    }))
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

    save() {
        const state = {
            length: this.length,
            cache: Array.from(this._rawCache.entries())
        };
        sessionStorage.setItem('lazyLocationState', JSON.stringify(state));
    }

    static load() {
        const savedStateJSON = sessionStorage.getItem('lazyLocationState');
        if (!savedStateJSON) {
            return null;
        }

        const savedState = JSON.parse(savedStateJSON);

        const newInstance = new LazyLocationData(savedState.length);
        newInstance._rawCache = new Map(savedState.cache);
        return newInstance;
    }
}