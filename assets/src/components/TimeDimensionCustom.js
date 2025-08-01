L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
    initialize: function(index, options) {
        const playerOptions = {
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