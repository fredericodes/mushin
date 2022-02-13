<template>
  <table class="buttons-div">
    <tr class="buttons-div">
      <td><button @click="this.$router.push('encrypt-file')" class="button">Encrypt file</button></td>
      <td><button @click="this.$router.push('decrypt-file')" class="button">Decrypt file</button></td>
    </tr>
  </table>
</template>

<style>
  .buttons-div {
    width: 100%;
  }

  .button {
    width: 100%;
    height: 100vh;
    background-color : transparent;
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

  .button:hover {
    color: #001F3F;
    background-color: #fffdd0;
  }
</style>