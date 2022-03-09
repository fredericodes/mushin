<template>
  <div>
    <form @submit.prevent="storePrivateSecretKeyInLocalStorage">
      <label for="secretKey">File Decryption: Enter private secret key</label>
      <input v-model="secretKey" type="text" id="secretKey" name="secretKey" placeholder="Enter private secret key for decryption...">

      <input v-on:click="storePrivateSecretKeyInLocalStorage" type="submit" value="Submit">
    </form>
    <button v-on:click="navigateToHomePage" class="homeBtn"><i class="fa fa-home"></i> Home</button>
  </div>
</template>

<script>

export default {
  name: "StoreSecretPrivateKey",

  data() {
    return {
      secretKey: "",
      message: ""
    };
  },

  methods: {
    async storePrivateSecretKeyInLocalStorage(){
      const secretKey = this.secretKey;
      if (this.secretKey === "") {
        await this.showSecretKeyNotProvidedErr()
      } else {
        try {
          localStorage.setItem("privateSecretKey", secretKey);
          await this.navigateToFileDecryptionUpload();
        } catch (err) {
          this.message = err.response.data().error;
        }
      }
    },

    async navigateToFileDecryptionUpload() {
      let base_url = window.location.origin
      let decryption_upload_url = "/decrypt-file"
      window.location.href = base_url+decryption_upload_url
    },

    async showSecretKeyNotProvidedErr() {
      await this.$swal.fire({
        icon: 'error',
        titleText: `File decryption`,
        text: `The private secret key was not provided for decryption.`
      })
    },

    async navigateToHomePage() {
      let base_url = window.location.origin
      window.location.href = base_url
    }
  }
}

</script>

<style>
.homeBtn {
  width: 100%;
  color: #fff;
  background-color: #231F20;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  font-size: large;
  border-radius: 40px;
}

.homeBtn:hover {
  color: black;
  background-color: #4CAF50;
}

input[type=text], select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type=submit] {
  width: 100%;
  color: #fff;
  background-color: #231F20;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  font-size: large;
  border-radius: 40px;
}

input[type=submit]:hover {
  color: black;
  background-color: #4CAF50;
}

div {
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
}
</style>