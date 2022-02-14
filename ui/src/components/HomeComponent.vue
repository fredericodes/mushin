<template>
  <table class="buttons-div">
    <tr class="buttons-div">
      <td><button v-on:click="redirect_to_encryption" class="btnMushin">Encrypt file</button></td>
      <td><button v-on:click="redirect_to_decryption" class="btnMushin">Decrypt file</button></td>
    </tr>
  </table>
</template>

<script>
export default {
  methods: {
    redirect_to_encryption: () => {
      let base_url = window.location.origin
      let encryption_status_url = "/encrypt-file"
      window.location.href = base_url+encryption_status_url
    },
    redirect_to_decryption: () => {
      let base_url = window.location.origin
      let decryption_status_url = "/decrypt-file"
      window.location.href = base_url+decryption_status_url
    },

  }
}
</script>

<style>
  .buttons-div {
    width: 100%;
    color: white;
  }

  .btnMushin {
    width: 100%;
    height: 100vh;
    background-color : #231F20;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: xxx-large;
    margin: 4px 2px;
    cursor: pointer;
  }

  .btnMushin:hover {
    color: #001F3F;
    background-color: #fff;
  }
</style>