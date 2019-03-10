<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Ваши успехи {{ username }}:</h2>
                    <p class="subtitle error-msg">{{ error }}</p>
                </div>
            </div>
        </section>

    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Progress extends Vue {
    private error: string = '';
    get username() {
        return this.$store.state.userData.username;
    }

    beforeMount() {
        const error = this.$store.dispatch('getProgress')
    }
}
</script>
