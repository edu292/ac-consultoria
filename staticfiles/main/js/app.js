import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: '/static/main/build/marker-icon-2x.png',
  iconUrl: '/static/main/build/marker-icon.png',
  shadowUrl: '/static/main/build/marker-shadow.png',
});
import 'leaflet.markercluster';
import 'iso8601-js-period';
import 'leaflet-timedimension';
import 'heatmap.js';
import HeatmapOverlay from 'leaflet-heatmap';

import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet-timedimension/dist/leaflet.timedimension.control.css';

import initMap from './map.js';

initMap(L, HeatmapOverlay);