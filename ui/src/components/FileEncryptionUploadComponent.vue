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
          Drag and drop your file here or click here to upload!
          <br>
          <br>
          Upload file upto 4 GB in size.
          <br>
          <br>
          The following file formats are supported for encryption.
          <br>
          <br>
        .jpg, .jpeg, .png, .gif, .pdf, .docx, .doc, .xls, .csv, .zip, mp3, mp4
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
</template>

<script>
import axios from 'axios'

export default {
  name: "Dropzone",

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
      } catch (err) {
        this.message = err.response.data().error;
        this.error = true;
        this.uploading = false;
      }
    }
  }
}

</script>

<style>
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