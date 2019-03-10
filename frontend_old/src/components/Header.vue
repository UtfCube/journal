<template>
<nav class="navbar is-light" role="navigation" aria-label="main navigation">
  <div class="navbar-menu">
    <div class="navbar-start">
      <router-link to="/" class="navbar-item">
        Домой
      </router-link>
      <router-link v-if="!isAuthenticated" :to="{ name: 'login' }" class="navbar-item">
        Войти
      </router-link>
      <router-link v-if="!isAuthenticated" :to="{ name: 'register' }" class="navbar-item">
        Регистрация
      </router-link>
    </div>
  </div>
</nav>
</template>

<script>
export default {
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    }
  }
}
</script>

<style>
</style>
