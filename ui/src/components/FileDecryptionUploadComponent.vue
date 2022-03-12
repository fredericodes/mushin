<template xmlns="http://www.w3.org/1999/html">
  <form @submit.prevent="sendFile" enctype="multipart/form-data">
    <div class="dropzone">
      <input
          type="file"
          class="input-file"
          ref="file"
          @change="sendFile"
      />

      <p v-if="!uploading" class="call-to-action">
        Drag and drop your .encrypted file here or click here to upload the .encrypted file for decryption!
      </p>

      <p v-for="file in uploadedFiles" :key="file.name">
        {{file.name}}
      </p>
      <p v-if="uploading" class="progress-bar">
        <progress
            class="progress is-primary"
            :value="progress"
            max="100"
        >
          {{progress}}</progress>
      </p>

      <p v-if="uploading" class="progress-percentage">
        {{progress}}% uploaded!
      </p>


    </div>
  </form>
  <button v-on:click="navigateToHomePage" class="homeBtn"><i class="fa fa-home"></i> Home</button>
</template>

<script>
import apiRoutes from "@/api/routes";
import apiClient from "@/api/client";

export default {
  name: "DecryptionDropZone",

  data() {
    return {
      file: "",
      message: "",
      error: false,
      uploading: false,
      uploadedFiles: [],
      progress: 0
    }
  },

  methods: {
    async sendFile(){
      const privateSecretKey = localStorage.getItem("privateSecretKey");
      const file = this.$refs.file.files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
        this.uploading = true;
        let uploadFileForDecryption = apiRoutes.UploadFileForDecryption
        const res = await apiClient.post(uploadFileForDecryption, formData, {
          onUploadProgress: e => this.progress = Math.round(e.loaded * 100 / e.total)
        })
        this.uploadedFiles.push(res.data.file);
        this.uploading = false;

        if (res.status === 200) {
          let decryptFile = apiRoutes.DecryptFile
          let urlParams = `?fileName=${res.data.fileName}&privateSecretKey=${privateSecretKey}`
          const response = await apiClient.put(decryptFile+urlParams)
          if (response.status === 200) {
            await this.showSuccessfulUpload(response.data.decryptionTrackingId)
            localStorage.clear()
            await this.navigateToDecryptionTracking()
          } else {
            await this.showFailedUpload()
            localStorage.clear()
            await this.navigateToStorePrivateKey()
          }
        } else {
          await this.showFailedUpload()
          localStorage.clear()
          await this.navigateToStorePrivateKey()
        }
      } catch (err) {
        this.message = err.response.data().error;
        this.error = true;
        this.uploading = false;
      }
    },

    async navigateToStorePrivateKey() {
      let base_url = window.location.origin
      let store_private_key_url = "/decrypt-file/private-key"
      window.location.href = base_url+store_private_key_url
    },

    async navigateToDecryptionTracking() {
      let base_url = window.location.origin
      let decryption_tracking_url = "/track-decryption"
      window.location.href = base_url+decryption_tracking_url
    },

    async showSuccessfulUpload(trackingId) {
      await this.$swal.fire({
        icon: 'success',
        titleText: `The file is now uploaded for decryption.`,
        html: `Track the file encryption status using the tracking id.
                 Copy tracking ID as it won't be shown again:
                 <b style="color: darkred">${trackingId}</b>`,
        confirmButtonText: "Go to tracking"
      })
    },

    async showFailedUpload() {
      let message = `The file upload was having issues.`
      this.$swal(message);
    },

    async navigateToHomePage() {
      let base_url = window.location.origin
      window.location.href = base_url
    }
  },

  beforeMount() {
    let privateSecretKey = localStorage.getItem("privateSecretKey");
    if (privateSecretKey === "" || privateSecretKey === null) {
      this.navigateToStorePrivateKey();
    }

  },
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

.dropzone {
  min-height: 200px;
  padding: 10px 10px;
  position: relative;
  cursor: pointer;
  outline: 2px dashed grey;
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
}

.input-file {
  opacity: 0;
  width: 100%;
  height: 200px;
  position: absolute;
  cursor: pointer;
}

.dropzone:hover {
  background: lightblue;
}

.dropzone .call-to-action {
  font-size: 1.2rem;
  text-align: center;
  padding: 50px 0;
}

.dropzone .progress-bar {
  text-align: center;
  padding: 70px 10px;
}

.progress-percentage {
  text-align: center;
}

</style>