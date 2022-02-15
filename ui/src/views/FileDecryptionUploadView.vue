<template>
  <div class="section">
    <div class="container">
      <FileDecryptionUploadComponent />
    </div>
  </div>
</template>

<script>
import FileDecryptionUploadComponent from '../components/FileDecryptionUploadComponent.vue'

export default {
  name: "App",
  components: { FileDecryptionUploadComponent }
}
</script>