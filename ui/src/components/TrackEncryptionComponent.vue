<template>
  <div>
    <form @submit.prevent="trackEncryptionStatus">
      <label for="trackingId">File Encryption Tracking ID</label>
      <input v-model="trackingId" type="text" id="trackingId" name="trackingId" placeholder="Enter tracking id...">

      <input v-on:click="trackEncryptionStatus" type="submit" value="Submit">
      <button v-on:click="navigateToHomePage" class="homeBtn"><i class="fa fa-home"></i> Home</button>
    </form>
  </div>
</template>

<script>
import apiRoutes from "@/api/routes";
import apiClient from "@/api/client";

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
          let getEncryptionStatus = apiRoutes.GetEncryptionStatus
          let urlParams = `?trackingId=${trackingId}`
          const response = await apiClient.get(getEncryptionStatus + urlParams)
          if (response.status === 200) {
            if (response.data.status === 'SUCCESS') {
              await this.showSuccessMessageWithEncryptedFileDownload(response.data)
              await this.downloadEncryptedFile(trackingId, response.data.fileName)
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
               Encryption key: <b style="color: darkred">${data.encryptionKey}</b>  <br><br>
               <b>
               Do not share the encryption key with anyone. <br>
               Save the encryption key safely to decrypt the encrypted file later.
               </b>
              `,
        confirmButtonText: "Download encrypted file"
      })
    },

    async showSuccessMessage(data) {
      await this.$swal.fire({
        icon: 'success',
        titleText: `Tracking status`,
        html: `Tracking id: ${data.encryptionTrackingId} <br><br>
               Status: ${data.status} <br><br>
               <b>The encryption process is still in ${data.status} status. Track status again later.</b>
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

    async downloadEncryptedFile(trackingId, fileName) {
      let encryptedFile = apiRoutes.GetEncryptedFile
      let urlParams = `?trackingId=${trackingId}`
      await apiClient({
        url: encryptedFile + urlParams,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${fileName}.encrypted`);
        document.body.appendChild(link);
        link.click();
      });
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