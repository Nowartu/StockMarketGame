<script setup>
import {authStore} from "@/stores/auth.js";
import {ref} from "vue";

const store = authStore()
const username = ref("")
const password = ref("")

async function login() {
  await store.login(username.value, password.value)
}

</script>

<template>
  <v-text-field v-model="username"></v-text-field>
  <v-text-field v-model="password" type="password"></v-text-field>
  <v-btn @click="login()"></v-btn>
   {{store}}
</template>

<style scoped lang="sass">

</style>
