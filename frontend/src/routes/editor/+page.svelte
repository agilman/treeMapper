<script>
  import { onMount, onDestroy} from 'svelte';
  import.meta.env.SSR ; 
  import moment from 'moment';

  let url = 'http://localhost:8000';

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
  let newTreeCoords=[];
  let newTreeLayer;
  let parkTreesLayer;
  let selectedTreeLayer;
  let toolTipLayer;
  let selectedTreeIndex=-1;
  let notes = [];
  let newNote = '';
  
  onMount(async function () {
    leaflet = await import('leaflet');

    const parkResponse = await fetch(url+"/api/parks");
    const myParks = await parkResponse.json();
    const mapboxToken = "pk.eyJ1IjoiYWdpbG1hbiIsImEiOiI3a05GVF9vIn0.c5pOjAXGeRPbv35PRmK90A";
    const myurl = "https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/{z}/{x}/{y}?access_token=" + mapboxToken;

    parks = myParks;
    if(parks.length){
      selectedPark=parks[0].id;

      map = leaflet.map(mapElement).setView([parks[0].lat,parks[0].lng], parks[0].zoom);
      leaflet.tileLayer(myurl, {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

      newTreeLayer = leaflet.layerGroup().addTo(map);
      parkTreesLayer = leaflet.layerGroup().addTo(map);
      selectedTreeLayer = leaflet.layerGroup().addTo(map);
      toolTipLayer = leaflet.layerGroup().addTo(map);
      map.on('click',mapClick);

      const resp = await fetch(url+"/api/trees/"+selectedPark);
      parkTrees = await resp.json();
      drawParkTrees();
    }
  
    const generaResponse = await fetch(url+"/api/genera");
    const myGenera = await generaResponse.json();
    genera = myGenera;
  });

  onDestroy(async () => {
    if(map) {
        console.log('Unloading Leaflet map.');
        map.remove();
    }
  });

  function mouseOverTree(e){
    const tid = e.target.treeId;
    let myTree;
    for (var i=0;i<parkTrees.length;i++){
      if(parkTrees[i].id==tid){
        myTree = parkTrees[i];
      }
    }

    //clear previous tooltip
    toolTipLayer.clearLayers();

    const mylatlng = {'lat': myTree.lat,'lng':myTree.lng}
    leaflet.tooltip().setLatLng(mylatlng).setContent(myTree.species.commonName).addTo(toolTipLayer);
  };

  function mouseOutofTree(e){
    toolTipLayer.clearLayers();
  };
  
  async function drawParkTrees(){
    parkTreesLayer.clearLayers();

    for(let i=0;i<parkTrees.length;i++){
      const myLatLng = [parkTrees[i].lat,parkTrees[i].lng];
      const myCircle = leaflet.circle(myLatLng,{
        radius:parkTrees[i].size
      })
      myCircle.treeId=parkTrees[i].id;
      myCircle.addTo(parkTreesLayer).on("click",treeClick).on('mouseover',mouseOverTree).on('mouseout',mouseOutofTree);
    }
  };

  async function treeClick(e){
    //This function is called when an established tree has been selected.:
    //  -highlight the tree on the map, center the map on it.
    //  -display tree info in side panel

    leaflet.DomEvent.stopPropagation(e); // prevent map from getting click event and drawing a new tree
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
        myCircle.on('mouseover',mouseOverTree).on('mouseout',mouseOutofTree).addTo(selectedTreeLayer);
        map.panTo(myLatLng);
      }
    } //end for
    
    newTreeCoords = [];
    newTreeLayer.clearLayers();

    //get notes
    const res = await fetch(url+"/api/notes/"+parkTrees[selectedTreeIndex].id);
    const myNotes = await res.json();
    
    notes = myNotes;
  };

  function changePark(){
    for(let i=0;i<parks.length;i++){
      if (parks[i].id == selectedPark){
        map.flyTo([parks[i].lat,parks[i].lng],parks[i].zoom);
      }
    }
    // drawParkTrees (no need, the function draws all the trees from all parks..)
    selectedTreeIndex = -1;
    notes= [];
    newTreeCoords=[];
    newTreeLayer.clearLayers();
    selectedTreeLayer.clearLayers();
  };

  async function changeGenus(){
    const resp = await fetch(url+"/api/species/"+selectedGenus);
    const mySpecies = await resp.json()
    species = mySpecies;
    selectedSpecies='';
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

    selectedTreeIndex = -1;
    selectedTreeLayer.clearLayers();
    notes = [];
    newNote = '';
  };

  async function saveTreeClick(){
    const data  = {park:selectedPark,
    species:selectedSpecies,
    lat: newTreeCoords[0],
    lng: newTreeCoords[1],
    size: radius};

    const res = await fetch(url+'/api/trees', {
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

    const res = await fetch(url+'/api/notes/'+myTree, {
			method: 'POST',
			body: JSON.stringify(data)});
    const myNote = await res.json();
    notes.push(myNote);
    notes = notes;
    newNote = '';
  };

  function convertTimeStamp(myTs){
    return moment(myTs).format('MM/DD/YYYY h:mmA');
  };
</script>
<div class="flex-row">
  <select name="parks" id="parks" bind:value={selectedPark} on:change={changePark} class="rounded-lg border mx-3 mt-1 p-2">
    {#each parks as park}
      <option value={park.id}>
        {park.name}
      </option>
    {/each}
  </select>
  <label for="mygeneras">
    New Tree:
  </label>
  <select name="genera" bind:value={selectedGenus} on:change={changeGenus} id="mygeneras" class="rounded-lg border mx-2 p-2">
    <option value='' selected disabled>Please select</option>
    {#each genera as genus}
      <option value={genus}>
          {genus}
      </option>
    {/each}
  </select>
  <select name="species" bind:value={selectedSpecies} class="rounded-lg mx-2 p-2">
    <option value='' disabled selected>Please select</option>
    {#each species as specie}
        <option value={specie.id}>
            {specie.species}
        </option>
    {/each}
  </select>
  <label for="radiusInput">Radius(meters):</label>
  <input onKeyDown="return false" size="4" type=number id="radiusInput" bind:value={radius} on:change={radiusChange} min=1 max=50 class="border rounded-lg mx-2 p-2">
  <button disabled={!newTreeCoords.length || !selectedSpecies} on:click={saveTreeClick} class="mx-2 p-2 bg-blue-300 rounded p-1 border border-gray-400 disabled:bg-gray-300">
    Save!
  </button>
</div>

<div class="flex items-start mt-2">
  <map-wrapper class="w-3/4">
    <div bind:this={mapElement} class="w-full h-full" style="height:500px"></div>
  </map-wrapper>
  <div class="flex-col w-1/4 items-start">
    {#if selectedTreeIndex > -1}
      <u><b>{parkTrees[selectedTreeIndex].species.commonName}</b></u> - 
      <a href="{parkTrees[selectedTreeIndex].species.wiki}">
        {parkTrees[selectedTreeIndex].species.genus}  {parkTrees[selectedTreeIndex].species.species}
      </a> 
      <br>
      <label for="treeNotes">Note:</label>
      <input type="text" maxlength="128" id="treeNotes" bind:value={newNote} class="rounded-lg border border-grey-400 m-2 p-1" >
      <button disabled={!newNote.length} on:click={saveNoteClick}
      class="m-2 p-2 bg-blue-300 rounded border border-grey-400 disabled:bg-gray-300">
      Save note</button>
      <br>
      <div>
      {#each notes as note}
        <div>
        {convertTimeStamp(note.ts)} - <p>{note.text}</p>
        <br>
        </div>
      {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  @import 'leaflet/dist/leaflet.css';
</style>