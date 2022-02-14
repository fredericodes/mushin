<template>
  <div class="section">
    <div class="container">
     <DropZone />

    </div>
  </div>
</template>

<script>
import DropZone from './DropZone.vue'

export default {
  name: "App",
  components: { DropZone }
}
</script>