<template>
  <div class="section">
    <div class="container">
      <TrackDecryptionComponent />
    </div>
  </div>
</template>

<script>
import TrackDecryptionComponent from '../components/TrackDecryptionComponent.vue'

export default {
  name: "App",
  components: { TrackDecryptionComponent }
}
</script>