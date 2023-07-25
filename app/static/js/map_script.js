// map_script.js

document.addEventListener('DOMContentLoaded', function () {
    const key = 'GI546B3SGnBV6vEau70S';
    const map = new maplibregl.Map({
        container: 'map',
        style: `https://api.maptiler.com/maps/167a5f44-80cd-4b4b-99e6-a49b98dc4f9b/style.json?key=${key}`,
        center: [-98.5795, 39.8282],
        zoom: 3,
    });

    map.on('load', () => {
        map.loadImage(
            'https://i.ibb.co/HCDh50Z/gps.png',// Add an image to use as a custom marker
            (error, image) => {
                if (error) throw error;
                map.addImage('custom-marker', image);

                // Load map_data.json using fetch and add the loaded JSON data as a source to the map
                fetch('/static/json/map_data.json') 
                    .then((response) => response.json())
                    .then((data) => { 
                        map.addSource('places', {
                            type: 'geojson',
                            data: data,
                        });

                        // Add a layer showing the places.
                        map.addLayer({
                            id: 'places',
                            type: 'symbol',
                            source: 'places',
                            layout: {
                                'icon-image': 'custom-marker', 
                                'icon-size': 0.8, 
                                'icon-allow-overlap': true, 
                            },
                        });
                    });
            }
        );

        // Create a popup, but don't add it to the map yet.
        const popup = new maplibregl.Popup({
            closeButton: false,
            closeOnClick: false
        });

        map.on('mouseenter', 'places', (e) => {
            // Change the cursor style as a UI indicator.
            map.getCanvas().style.cursor = 'pointer';

            const coordinates = e.features[0].geometry.coordinates.slice();
            const description = e.features[0].properties.description;

            // Ensure that if the map is zoomed out such that multiple
            // copies of the feature are visible, the popup appears
            // over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            // Populate the popup and set its coordinates
            // based on the feature found.
            popup.setLngLat(coordinates).setHTML(description).addTo(map);
        });

        map.on('mouseleave', 'places', () => {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
    });
});
