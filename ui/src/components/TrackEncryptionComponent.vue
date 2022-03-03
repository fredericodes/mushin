<template>
  <div>
    <form @submit.prevent="trackEncryptionStatus">
      <label for="trackingId">File Encryption Tracking ID</label>
      <input v-model="trackingId" type="text" id="trackingId" name="trackingId" placeholder="Enter tracking id...">

      <input v-on:click="trackEncryptionStatus" type="submit" value="Submit">
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "TrackEncryption",

  data() {
    return {
      trackingId: "",
      message: ""
    };
  },

  methods: {
    async trackEncryptionStatus(){
      const trackingId = this.trackingId;
      if (this.trackingId === "") {
        this.showTrackingIdNotProvidedErr()
      } else {
        try {
          const response = await axios.get(`http://localhost:10000/encryption/status?trackingId=${trackingId}`)
          if (response.status === 200) {
            this.showSuccessMessage(response.data.encryptionTrackingId)
          } else {
            this.showTrackingIdNotProvidedErr()
          }
        } catch (err) {
          this.message = err.response.data().error;
        }
      }
    },

    showSuccessMessage(trackingId) {
      this.$swal.fire({
        icon: 'success',
        titleText: `The file is now uploaded for encryption.`,
        text: `Track the file encryption status using the tracking id: ${trackingId}`
      })
    },

    showTrackingIdNotProvidedErr() {
      this.$swal.fire({
        icon: 'error',
        titleText: `File encryption tracking`,
        text: `The file encryption tracking id was not provided.`
      })
    },
  }
}

</script>

<style>
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