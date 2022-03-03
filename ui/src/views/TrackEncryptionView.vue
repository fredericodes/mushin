<template>
  <div class="section">
    <div class="container">
      <TrackEncryptionComponent />
    </div>
  </div>
</template>

<script>
import TrackEncryptionComponent from '../components/TrackEncryptionComponent.vue'

export default {
  name: "App",
  components: { TrackEncryptionComponent }
}
</script>