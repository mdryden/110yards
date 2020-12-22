<script type="ts">
    import {register} from "./Router.svelte"
    export let path = "/";
    export let component = null;
</script>

<svelte:component this="{component}" />
<slot />