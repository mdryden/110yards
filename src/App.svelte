<script type="ts">
	import router from "page"

	import Home from "./components/Home.svelte"
	import About from "./components/About.svelte"

	// let page;
	// let params;

	// router("/", () => page = Home);
	// router("/about", () => page = About);
	// router.start();

	export let version = "1.0.0"
	export let lastUpdated = "a while ago"
</script>

<main>
	<!-- Todo own file-->
	<nav>
		<a href="/">home</a>
		<a href="/about">about</a>
	</nav>

	<svelte:component this="{page}" params="{params}" />

	<div class="container" id="body" data-version="{version}">
	<div id="footer">
		<p>&copy; 2021 Michael Dryden</p>
		<p title="Version {version}">Last release {lastUpdated}</p>
	</div>
	</div>
</main>

<style>
	
</style>