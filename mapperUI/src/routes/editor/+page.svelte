<h3>Hello</h3>
<label for="parks">Parks:</label>

<select name="parks" id="parks">
  <option value=1>Elizabet Park</option>
  <option value=2>Memorial Park</option>
  <option value=3>Broadway Park</option>
</select> 
<br>

<select name="genera">
    <option selected disabled>Please select </option>
    {#each genera as genus}
        <option value={genus}>
            {genus}
        </option>
    {/each}
</select>

<script>
import { onMount } from 'svelte';

let genera = [] 

onMount(async function () {
  const response = await fetch("http://localhost:8000/api/genera");
  const myGenera = await response.json();
  genera = myGenera;
});
</script>