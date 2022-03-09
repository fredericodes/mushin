<template>
  <div>
    <form @submit.prevent="trackDecryptionStatus">
      <label for="trackingId">File Decryption Tracking ID</label>
      <input v-model="trackingId" type="text" id="trackingId" name="trackingId" placeholder="Enter tracking id...">

      <input v-on:click="trackDecryptionStatus" type="submit" value="Submit">
      <button v-on:click="navigateToHomePage" class="homeBtn"><i class="fa fa-home"></i> Home</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "TrackDecryption",

  data() {
    return {
      trackingId: "",
      message: ""
    };
  },

  methods: {
    async trackDecryptionStatus(){
      const trackingId = this.trackingId;
      if (this.trackingId === "") {
        await this.showTrackingIdNotProvidedErr()
      } else {
        try {
          const response = await axios.get(`http://localhost:10000/decryption/status?trackingId=${trackingId}`)
          if (response.status === 200) {
            if (response.data.status === 'SUCCESS') {
              await this.showSuccessMessageWithDecryptedFileDownload(response.data)
              await this.downloadDecryptedFile(trackingId, response.data.fileName)
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

    async showSuccessMessageWithDecryptedFileDownload(data) {
      await this.$swal.fire({
        icon: 'success',
        titleText: `Tracking status`,
        html: `Tracking id: ${data.decryptionTrackingId} <br><br>
               Status: ${data.status}  <br><br>
              `,
        confirmButtonText: "Download decrypted file"
      })
    },

    async showSuccessMessage(data) {
      await this.$swal.fire({
        icon: 'success',
        titleText: `Tracking status`,
        html: `Tracking id: ${data.decryptionTrackingId} <br><br>
               Status: ${data.status} <br><br>
               <b>The decryption process is still in ${data.status} status. Track status again later.</b>
              `
      })
    },

    async showTrackingIdNotProvidedErr() {
      await this.$swal.fire({
        icon: 'error',
        titleText: `File decryption tracking`,
        text: `The file decryption tracking id was not provided.`
      })
    },

    async downloadDecryptedFile(trackingId, fileName) {
      await axios({
        url: `http://localhost:10000/decrypted?trackingId=${trackingId}`,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${fileName}`);
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