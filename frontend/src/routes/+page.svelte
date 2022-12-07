<script>
    import { onMount, onDestroy} from 'svelte';
    import moment from 'moment';
  
    import { env } from '$env/dynamic/private';
    console.log('backend url', env.BACKEND_URL);
    let url = env.BACKEND_URL;
  
    let L; // L : All types: map, circle, groupLayer etc
    let map;
    let parks = [];
    let selectedPark;
    let parkTrees = [];
    let newTreeLayer;
    let parkTreesLayer;
    let selectedTreeLayer;
    let toolTipLayer;
    let selectedTreeIndex=-1;
    let notes = [];
    let newNote = '';
    
    onMount(async function () {
      L = await import('leaflet');
  
      const parkResponse = await fetch(url+"/api/parks");
      const myParks = await parkResponse.json();
      const mapboxToken = "pk.eyJ1IjoiYWdpbG1hbiIsImEiOiI3a05GVF9vIn0.c5pOjAXGeRPbv35PRmK90A";
      const myurl = "https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/{z}/{x}/{y}?access_token=" + mapboxToken;
  
      parks = myParks;
      if(parks.length){
        selectedPark=parks[0].id;
  
        map = L.map('map').setView([parks[0].lat,parks[0].lng], parks[0].zoom);
        L.tileLayer(myurl, {
              attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          }).addTo(map);
  
        newTreeLayer = L.layerGroup().addTo(map);
        parkTreesLayer = L.layerGroup().addTo(map);
        selectedTreeLayer = L.layerGroup().addTo(map);
        toolTipLayer = L.layerGroup().addTo(map);
        map.on('click',mapClick);
  
        const resp = await fetch(url+"/api/trees/"+selectedPark);
        parkTrees = await resp.json();
        drawParkTrees();
      }
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
      L.tooltip().setLatLng(mylatlng).setContent(myTree.species.commonName).addTo(toolTipLayer);
    };
  
    function mouseOutofTree(e){
      toolTipLayer.clearLayers();
    };
    
    async function drawParkTrees(){
      parkTreesLayer.clearLayers();
  
      for(let i=0;i<parkTrees.length;i++){
        const myLatLng = [parkTrees[i].lat,parkTrees[i].lng];
        const myCircle = L.circle(myLatLng,{
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
  
      L.DomEvent.stopPropagation(e); // prevent map from getting click event and drawing a new tree
      selectedTreeLayer.clearLayers();
      
      for(let i=0;i<parkTrees.length;i++){
        if (parkTrees[i].id == e.sourceTarget.treeId){
          selectedTreeIndex = i;
  
          const myLatLng = [parkTrees[i].lat,parkTrees[i].lng];
          const myCircle = L.circle(myLatLng,{
            radius:parkTrees[i].size,
            color:'red'
           });
          myCircle.treeId=parkTrees[i].id;
          myCircle.on('mouseover',mouseOverTree).on('mouseout',mouseOutofTree).addTo(selectedTreeLayer);
          map.panTo(myLatLng);
        }
      } //end for
  
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
      selectedTreeLayer.clearLayers();
    };
  
    
    function mapClick(e){  
      selectedTreeIndex = -1;
      selectedTreeLayer.clearLayers();
      notes = [];
      newNote = '';
    };
  
    function convertTimeStamp(myTs){
      return moment(myTs).format('MM/DD/YYYY h:mmA');
    };
    
    
  </script>
  <div class="flex justify-between p-3 bg-cyan-900 h-1/6 text-slate-200 font-sans font-bold text-2xl items-center">
    <div class="font-extrabold text-3xl">
      <a href="https://www.agilman.org">Alex Gilman</a>
      |
      <a href="/">Tree Mapper</a>
    </div>
    <div class="flex align-end">
    <div class="px-3"><a href="/editor">Editor</a></div>
    <div class="px-2"><a href="/about">About</a></div>
    </div>
  </div>
  <div class="flex-row">
    <select name="parks" id="parks" bind:value={selectedPark} on:change={changePark} class="rounded-lg border mx-3 mt-1 p-2">
      {#each parks as park}
        <option value={park.id}>
          {park.name}
        </option>
      {/each}
    </select>
  </div>
  
  <div class="flex items-start mt-2">
    <map-wrapper class="w-3/4">
      <div id='map' class="w-full h-full" style="height:500px"></div>
    </map-wrapper>
    <div class="flex-col w-1/4 items-start">
      {#if selectedTreeIndex > -1}
        <a href="{parkTrees[selectedTreeIndex].species.wiki}">
        <u><b>{parkTrees[selectedTreeIndex].species.commonName}</b></u> - 
          {parkTrees[selectedTreeIndex].species.genus}  {parkTrees[selectedTreeIndex].species.species}
        </a>
      {/if}
    </div>
  </div>
  
  <style>
    @import 'leaflet/dist/leaflet.css';
  </style>