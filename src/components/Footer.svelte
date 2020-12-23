<script type="ts">
  export let version = "1.0.0"
  export let lastUpdated = "a while ago"
</script>

<style>
  #footer {
    padding-top: 2em;
    margin: auto;
    width: 50%;
    text-align: center;
    font-size: small;
    color: gray;
  }
</style>

<div class="container" id="body" data-version={version}>
  <div id="footer">
    <p>&copy; 2021 Michael Dryden</p>
    <p title="Version {version}">Last release {lastUpdated}</p>
  </div>
</div>
