<script>
    import { onMount, onDestroy } from 'svelte';
    import.meta.env.SSR

    let mapElement;
    let map;

    onMount(async () => {

        const leaflet = await import('leaflet');
        48.760002485861406, -122.49076485842225
        map = leaflet.map(mapElement).setView([48.76000, -122.490773], 18);

        leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
    });

    onDestroy(async () => {
        if(map) {
            console.log('Unloading Leaflet map.');
            map.remove();
        }
    });
</script>


<main>
    <div bind:this={mapElement}></div>
</main>

<style>
    @import 'leaflet/dist/leaflet.css';
    main div {
        height: 400px;
    }
</style>
