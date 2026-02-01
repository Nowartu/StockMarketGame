<script setup>
import { apiFetch } from "@/utils/apiFetch.js";
import {onMounted, ref} from "vue";

const companies = ref([])

async function fetchCompanies() {
  companies.value = await apiFetch("/api/companies/");
}
onMounted(fetchCompanies);
</script>

<template>
  {{ companies }}
</template>

<style scoped lang="sass">

</style>
