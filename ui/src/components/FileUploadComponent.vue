<template>
    <div id="app">
      <dashboard :uppy="uppy" :props="{theme: 'light'}"/>
    </div>
</template>

<script>
  import {Dashboard} from '@uppy/vue'
  import Uppy from '@uppy/core'
  import Tus from '@uppy/tus'
  import '@uppy/core/dist/style.css'
  import '@uppy/dashboard/dist/style.css'

  export default {
    name: 'App',
    components: {
      Dashboard
    },
    computed: {
      uppy: () => new Uppy({
        restrictions:{
          maxNumberOfFiles: 1
        }
      }).use(Tus, {
        endpoint: 'https://tusd.tusdemo.net/files/', // use your tus endpoint here
        retryDelays: [0, 1000, 3000, 5000],
      }).on('upload-success', result => {
        if(window.confirm("The file is now uploaded. Click Ok to see the download status of your file encryption or decryption.")) {
          let base_url = window.location.origin
          let encryption_status_url = "/"
          console.log(base_url+encryption_status_url)
          window.location.href = base_url+encryption_status_url
        }
      })
    },
    beforeDestroy() {
      this.uppy.close()
    }

  }
</script>