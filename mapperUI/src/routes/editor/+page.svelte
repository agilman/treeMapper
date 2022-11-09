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
<p>{commonName}</p>
<p>{wiki}</p>

<LeafletMap />

<script>
import { onMount } from 'svelte';
import LeafletMap from '$lib/LeafletMap.svelte';

let parks = [];
let selectedPark;
let parkCenter = [];
let parkZoom =18;
let genera = [] ;
let selectedGenus;
let species = [];
let selectedSpecies;
let commonName=''; 
let wiki = '';

onMount(async function () {
  const parkResponse = await fetch("http://localhost:8000/api/parks");
  const myParks = await parkResponse.json();

  parks = myParks;
  if(parks.length){
    selectedPark=parks[0].id;
    parkCenter = [parks[0].lat,parks[0].lng];
    parkZoom = parks[0].zoom;
  }

  const generaResponse = await fetch("http://localhost:8000/api/genera");
  const myGenera = await generaResponse.json();
  genera = myGenera;
});

async function changePark(){
  console.log('changed park');
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
</script>