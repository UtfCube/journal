<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Здравствуйте, {{ username }}</h2>
                    <p class="subtitle error-msg">{{ error }}</p>
                </div>
            </div>
        </section>
        <ul>
            <li v-for="subject in subjects" :key="subject.id" @click="click(subject)">
                {{subject}}
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class StudentHome extends Vue {
    private error: string = '';
    
    get username() {
        return this.$store.state.userData.username;
    }

    get subjects() {
        return this.$store.state.userData.info.subjects;
    }
    beforeMount () {
        const error = this.$store.dispatch('getStudentHome');
    }

    click(subject) {
        this.$router.push({ name: 'progress', params: { subject: subject}})
    }
}
</script>

<!--
<script>
import axios from 'axios'

export default {
    name: 'student-home',
    computed: {
        username () {
            return this.$store.state.userData.username;
        },
        subjects () {
            return this.$store.state.userData.info.subjects;
        }
    },
    beforeMount () {
        const error = this.$store.dispatch('getStudentHome');
        if (error) {
            alert(error)
        }
    },
    watch: {
    },
    methods: {
    }
}
</script>
-->

