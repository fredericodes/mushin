<template xmlns="http://www.w3.org/1999/html">
  <label>File Encryption: Upload a file for encryption</label>
  <br><br>
  <form @submit.prevent="sendFile" enctype="multipart/form-data">
    <div class="dropzone">
      <input
          type="file"
          class="input-file"
          ref="file"
          @change="sendFile"
      />

      <p v-if="!uploading" class="call-to-action">
          Drag and drop your file here or click here to upload!
          <br>
          <br>
          Upload file upto 4 GB in size.
          <br>
          <br>
          The following file formats are supported for encryption.
          <br>
          <br>
        .txt, .jpg, .jpeg, .png, .gif, .pdf, .docx, .doc, .xls, xlsx, .csv, .csv1, .zip, .mp3, .tif, .tiff
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
  <br>
  <button v-on:click="navigateToHomePage" class="homeBtn"><i class="fa fa-home"></i> Home</button>
</template>

<script>
import axios from 'axios'

export default {
  name: "EncryptionDropZone",

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
      const file = this.$refs.file.files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
        this.uploading = true;
        const res = await axios.post('http://localhost:10000/encryption/upload', formData, {
          onUploadProgress: e => this.progress = Math.round(e.loaded * 100 / e.total)
        })
        this.uploadedFiles.push(res.data.file);
        this.uploading = false;

        if (res.status === 200) {
          await this.showSuccessfulUpload(res.data.encryptionTrackingId)
          await this.navigateToEncryptionTrackingPage()
        } else {
          await this.showFailedUpload()
        }

      } catch (err) {
        this.message = err.response.data().error;
        this.error = true;
        this.uploading = false;
        await this.showFailedUpload()
      }
    },

    async showSuccessfulUpload(trackingId) {
      await this.$swal.fire({
          icon: 'success',
          titleText: `The file is now uploaded for encryption.`,
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

    async navigateToEncryptionTrackingPage() {
      let base_url = window.location.origin
      let encryption_tracking_url = "/track-encryption"
      window.location.href = base_url+encryption_tracking_url
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