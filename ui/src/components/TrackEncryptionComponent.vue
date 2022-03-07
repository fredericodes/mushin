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
import { v4 as uuidV4 } from 'uuid';

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
        await this.showTrackingIdNotProvidedErr()
      } else {
        try {
          const response = await axios.get(`http://localhost:10000/encryption/status?trackingId=${trackingId}`)
          if (response.status === 200) {
            if (response.data.status === 'SUCCESS') {
              await this.showSuccessMessageWithEncryptedFileDownload(response.data)
              await this.downloadEncryptedFile(trackingId)
            } else {
              await this.showSuccessMessage(response.data)
            }
          } else {
            await this.showTrackingIdNotProvidedErr()
          }
        } catch (err) {
          this.message = err.response.data().error;
        }
      }
    },

    async showSuccessMessageWithEncryptedFileDownload(data) {
      await this.$swal.fire({
        icon: 'success',
        titleText: `Tracking status`,
        html: `Tracking id: ${data.encryptionTrackingId} <br><br>
               Status: ${data.status}  <br><br>
               Encryption key: ${data.encryptionKey}  <br><br>
               Do not share the encryption key with anyone. <br>
               Save the encryption key safely to decrypt the encrypted file later.
              `,
        confirmButtonText: "Download encrypted file"
      })
    },

    async showSuccessMessage(data) {
      await this.$swal.fire({
        icon: 'success',
        titleText: `Tracking status`,
        text: `Tracking id: ${data.encryptionTrackingId}
               Status: ${data.status}
              `
      })
    },

    async showTrackingIdNotProvidedErr() {
      await this.$swal.fire({
        icon: 'error',
        titleText: `File encryption tracking`,
        text: `The file encryption tracking id was not provided.`
      })
    },

    async downloadEncryptedFile(trackingId) {
      await axios({
        url: `http://localhost:10000/encrypted?trackingId=${trackingId}`,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${uuidV4()}.encrypted`);
        document.body.appendChild(link);
        link.click();
      });
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