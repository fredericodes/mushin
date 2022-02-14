<template>
  <div class="section">
    <div class="container">
     <DropZoneComponent />

    </div>
  </div>
</template>

<script>
import DropZoneComponent from '../components/DropZoneComponent.vue'

export default {
  name: "App",
  components: { DropZoneComponent }
}
</script>