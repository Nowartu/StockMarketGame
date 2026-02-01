import { defineStore } from "pinia";

const API_URL = 'http://localhost:8000';

export const authStore = defineStore("auth", {
  state: () => ({
    access: localStorage.getItem("accessToken"),
    refresh: localStorage.getItem("refreshToken"),
    user: null,
  }),
  getters: {

  },
  actions: {
    async login(username, password) {
      const response = await fetch(`${API_URL}/api/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "username": username, "password": password }),
      })

      if (!response.ok) {
        throw new Error("Invalid credentials");
      }

      const data = await response.json();

      this.access = data.access;
      this.refresh = data.refresh;

      localStorage.setItem("accessToken", data.access);
      localStorage.setItem("refreshToken", data.refresh);

    },

    async refreshToken(){
      const response = await fetch(`${API_URL}/api/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({refresh: this.refreshToken}),
      })

      if (!response.ok) {
        await this.logout()
        throw new Error("Token expired");
      }

      const data = await response.json();
      this.access = data.access;
      localStorage.setItem("accessToken", data.access);
    },

    async logout(){
      this.access = null
      this.refresh = null
      this.user = null
      localStorage.clear()
    }
  }
})
