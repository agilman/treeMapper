<script>
    import { onMount, onDestroy, tick } from 'svelte';
    import.meta.env.SSR

    export let mapCenter;
    export let mapZoom;
    
    let mapElement;
    let map;
    onMount(async () => {
        await tick();
        await tick();
        const leaflet = await import('leaflet');
        console.log('about to onmount map center', mapCenter);
        map = leaflet.map(mapElement).setView(mapCenter, mapZoom);

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
