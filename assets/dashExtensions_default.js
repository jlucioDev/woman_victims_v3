window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng, map) {
            map.flyTo(latlng, 10);
            return L.popup().setContent(feature.properties.name);
        }
    }
});