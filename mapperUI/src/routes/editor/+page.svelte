<h3>Hello</h3>
<label for="parks">Parks:</label>

<select name="parks" id="parks">
  <option value=1>Elizabet Park</option>
  <option value=2>Memorial Park</option>
  <option value=3>Broadway Park</option>
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

<select name="species" bind:value={selectedSpecies}>
  <option selected disabled>Please select </option>
  {#each species as specie}
      <option value={specie.id}>
          {specie.species}
      </option>
  {/each}
</select>


<script>
import { onMount } from 'svelte';

let genera = [] ;
let selectedGenus;
let species = [];
let selectedSpecies;

onMount(async function () {
  const response = await fetch("http://localhost:8000/api/genera");
  const myGenera = await response.json();
  genera = myGenera;
});

async function changeGenus(){
  const resp = await fetch("http://localhost:8000/api/species/"+selectedGenus);
  const mySpecies = await resp.json()
  species = mySpecies;
  selectedSpecies='';
}
</script>