<template>
    <div>
        <h1>Здравствуйте, {{username}}</h1>
        <ul>
            <li v-for="subject in subjects" :key="subject.id">
                {{subject}}
            </li>
        </ul>
    </div>
</template>

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


