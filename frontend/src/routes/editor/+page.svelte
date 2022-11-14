<script>
  import { onMount, onDestroy} from 'svelte';
  import.meta.env.SSR

  let leaflet; // L : All leaflet types: map, circle, groupLayer etc
  let mapElement; //Binds to the <div> containing the map
  let map;
  
  let parks = [];
  let selectedPark;
  let genera = [] ;
  let selectedGenus='';
  let species = [];
  let selectedSpecies='';
  let parkTrees = [];
  let radius=10;
  let commonName=''; 
  let newTreeCoords=[];
  let newTreeLayer;
  let parkTreesLayer;
  let selectedTreeLayer;
  let selectedTreeIndex=-1;
  let notes = [];
  let newNote = '';
  
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
      parkTreesLayer = leaflet.layerGroup().addTo(map);
      selectedTreeLayer = leaflet.layerGroup().addTo(map);
      map.on('click',mapClick);

      const resp = await fetch("http://localhost:8000/api/trees/"+selectedPark);
      parkTrees = await resp.json();
      drawParkTrees();
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
  
  async function drawParkTrees(){
    parkTreesLayer.clearLayers();

    for(let i=0;i<parkTrees.length;i++){
      const myLatLng = [parkTrees[i].lat,parkTrees[i].lng];
      const myCircle = leaflet.circle(myLatLng,{
        radius:parkTrees[i].size
      })
      myCircle.treeId=parkTrees[i].id;
      myCircle.addTo(parkTreesLayer).on("click",treeClick);
    }
  };

  function treeClick(e){
    leaflet.DomEvent.stopPropagation(e);
    selectedTreeLayer.clearLayers();
    
    for(let i=0;i<parkTrees.length;i++){
      if (parkTrees[i].id == e.sourceTarget.treeId){
        selectedTreeIndex = i;

        const myLatLng = [parkTrees[i].lat,parkTrees[i].lng];
        const myCircle = leaflet.circle(myLatLng,{
          radius:parkTrees[i].size,
          color:'red'
         });
        myCircle.treeId=parkTrees[i].id;
        myCircle.addTo(selectedTreeLayer);

        map.panTo(myLatLng);
      }
    };
  };
  function changePark(){
    for(let i=0;i<parks.length;i++){
      if (parks[i].id == selectedPark){
        map.flyTo([parks[i].lat,parks[i].lng],parks[i].zoom);
      }
    }
    // drawParkTrees (no need, the function draws all the trees from all parks..)
  };

  async function changeGenus(){
    const resp = await fetch("http://localhost:8000/api/species/"+selectedGenus);
    const mySpecies = await resp.json()
    species = mySpecies;
    selectedSpecies='';
    commonName = '';
  };
  
  //commonName not displayed, this is not needed...
  function changeSpecies(){
   for (let i=0; i<species.length; i++){
    if (species[i].id === selectedSpecies){
        commonName = species[i].commonName;
      }
    }
  };

  function redrawNewTree(){
    newTreeLayer.clearLayers();
    var circle = leaflet.circle(newTreeCoords, {
      color: 'green',
      fillColor: '#1f9520',
      fillOpacity: 0.5,
      radius: radius
    }).addTo(newTreeLayer);
  };
  
  function mapClick(e){
    const mylatlng = [e.latlng['lat'],e.latlng['lng']];
    newTreeCoords = mylatlng;
    redrawNewTree();
  };

  async function saveTreeClick(){
    const data  = {park:selectedPark,
    species:selectedSpecies,
    lat: newTreeCoords[0],
    lng: newTreeCoords[1],
    size: radius};

    const res = await fetch('http://localhost:8000/api/trees', {
			method: 'POST',
			body: JSON.stringify(data)});
    const myTree = await res.json()
    parkTrees.push(myTree);
    newTreeLayer.clearLayers();
    drawParkTrees();
    newTreeCoords=[];
  };

  async function radiusChange(){
    redrawNewTree();
  };

  async function saveNoteClick(){
    const myTree = parkTrees[selectedTreeIndex].id;
    const data  = {tree:myTree, text: newNote};

    const res = await fetch('http://localhost:8000/api/notes/'+myTree, {
			method: 'POST',
			body: JSON.stringify(data)});
    const myNote = await res.json()
    console.log("saved note:", myNote)
    notes.push(myNote);

    newNote = '';
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
    <option value='' selected disabled>Please select</option>
    {#each genera as genus}
        <option value={genus}>
            {genus}
        </option>
    {/each}
</select>

<select name="species" bind:value={selectedSpecies} on:change={changeSpecies}>
  <option value='' disabled selected>Please select</option>
  {#each species as specie}
      <option value={specie.id}>
          {specie.species}
      </option>
  {/each}
</select>
<label for="radiusInput">Radius(meters):</label>
<input type=number id="radiusInput" bind:value={radius} on:change={radiusChange} min=1 max=100>
<button disabled={!newTreeCoords.length || !selectedSpecies} on:click={saveTreeClick} class="m-1 bg-blue-300 rounded p-1 border border-gray-400 disabled:bg-gray-300">
  Save!
</button>
<div class="flex items-start">
  <map-wrapper class="flex w-3/4">
    <div bind:this={mapElement} class="flex-auto" style="height:400px"></div>
  </map-wrapper>
  <div class="flex-col items-start">
   {#if selectedTreeIndex > -1}
    <h2><u><b>{parkTrees[selectedTreeIndex].species.commonName}</b></u></h2>
      {parkTrees[selectedTreeIndex].species.genus}  {parkTrees[selectedTreeIndex].species.species}
      <br>
      {parkTrees[selectedTreeIndex].species.wiki}
      <br>
      <label for="notes">Notes:</label>
      <input type="text" id="notes" class="border border-grey-400" bind:value={newNote}>
      <button disabled={!newNote.length}
       on:click={saveNoteClick}
       class="m-1 bg-blue-300 rounded p-1 border border-grey-400 disabled:bg-gray-300">Save notes</button>
       <br>
       <div>
        {notes}
       </div>
    {/if}
  </div>
</div>

<style>
  @import 'leaflet/dist/leaflet.css';
</style>