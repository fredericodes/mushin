<template>
  <div class="section">
    <div class="container">
     <FileEncryptionUploadComponent />
    </div>
  </div>
</template>

<script>
import FileEncryptionUploadComponent from '../components/FileEncryptionUploadComponent.vue'

export default {
  name: "App",
  components: { FileEncryptionUploadComponent }
}
</script>