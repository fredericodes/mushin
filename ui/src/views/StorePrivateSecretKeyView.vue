<template>
  <div class="section">
    <div class="container">
      <StorePrivateSecretKeyComponent />
    </div>
  </div>
</template>

<script>
import StorePrivateSecretKeyComponent from '../components/StorePrivateSecretKeyComponent.vue'

export default {
  name: "App",
  components: { StorePrivateSecretKeyComponent }
}
</script>