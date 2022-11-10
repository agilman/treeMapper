<script>
  import { onMount, onDestroy} from 'svelte';
  import.meta.env.SSR

  let leaflet;

  let mapElement;
  let map;
  
  let parks = [];
  let selectedPark;
  let genera = [] ;
  let selectedGenus;
  let species = [];
  let selectedSpecies;
  let radius=10;
  let commonName=''; 
  let wiki = '';
  let newTreeCoords=[];
  let newTreeLayer;
  
  onMount(async function () {
    leaflet = await import('leaflet');

    const parkResponse = await fetch("http://localhost:8000/api/parks");
    const myParks = await parkResponse.json();
  
    parks = myParks;
    if(parks.length){
      selectedPark=parks[0].id;

      map = leaflet.map(mapElement).setView([parks[0].lat,parks[0].lng], parks[0].zoom);
      leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

      newTreeLayer = leaflet.layerGroup().addTo(map);
      map.on('click',mapClick);
    }
  
    const generaResponse = await fetch("http://localhost:8000/api/genera");
    const myGenera = await generaResponse.json();
    genera = myGenera;
  });

  onDestroy(async () => {
        if(map) {
            console.log('Unloading Leaflet map.');
            map.remove();
        }
    });
  
  function changePark(){
    for(let i=0;i<parks.length;i++){
      if (parks[i].id == selectedPark){
        map.flyTo([parks[i].lat,parks[i].lng],parks[i].zoom);
      }
    }
  };

  async function changeGenus(){
    const resp = await fetch("http://localhost:8000/api/species/"+selectedGenus);
    const mySpecies = await resp.json()
    species = mySpecies;
    selectedSpecies='';
    commonName = '';
    wiki = '';
  };
  
  function changeSpecies(){
   for (let i=0; i<species.length; i++){
    if (species[i].id === selectedSpecies){
        commonName = species[i].commonName;
        wiki = species[i].wiki;
      }
    }
  };

  function mapClick(e){
    const mylatlng = [e.latlng['lat'],e.latlng['lng']];
    newTreeCoords = mylatlng;
    newTreeLayer.clearLayers();
    var circle = leaflet.circle(mylatlng, {
      color: 'green',
      fillColor: '#1f9520',
      fillOpacity: 0.5,
      radius: radius
    }).addTo(newTreeLayer);
  };
  async function saveClick(){
    const data  = {park:selectedPark,
    species:selectedSpecies,
    lat: newTreeCoords[0],
    lng: newTreeCoords[1],
    size: radius};

    const res = await fetch('http://localhost:8000/api/trees', {
			method: 'POST',
			body: JSON.stringify(data)});
  };
  </script>

<h3>Hello, Welcome to Tree Mapper!</h3>
<label for="parks">Parks:</label>

<select name="parks" id="parks" bind:value={selectedPark} on:change={changePark}>
  {#each parks as park}
    <option value={park.id}>
      {park.name}
    </option>
  {/each}
</select> 
<br>

<select name="genera" bind:value={selectedGenus} on:change={changeGenus}>
    <option selected disabled>Please select </option>
    {#each genera as genus}
        <option value={genus}>
            {genus}
        </option>
    {/each}
</select>

<select name="species" bind:value={selectedSpecies} on:change={changeSpecies}>
  <option selected disabled>Please select </option>
  {#each species as specie}
      <option value={specie.id}>
          {specie.species}
      </option>
  {/each}
</select>
<label for="radiusInput">Radius(meters):</label>
<input type=number id="radiusInput" bind:value={radius} min=1 max=100>
<button on:click={saveClick}>
  Save!
</button>
<p>{commonName}</p>
<p>{wiki}</p>

<map-wrapper>
  <div bind:this={mapElement}></div>
</map-wrapper>

<style>
  @import 'leaflet/dist/leaflet.css';
  map-wrapper div {
      height: 400px;
  }
</style>