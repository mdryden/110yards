<script context="module" type="ts">
    const routes: {[key: string]: object} = {}

    export interface RouteConfig {
        path: string,
        component: object
    }

    export function register(route: RouteConfig) {
        routes[route.path] = route;
    }
</script>

<script type="ts">
    import { onMount } from "svelte"
    import page from "page"

    onMount(() => console.log(routes));

</script>

<slot />