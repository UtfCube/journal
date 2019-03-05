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
    data: function () {
        return {
            username: '',
            subjects: {}
        }
    },
    created() {
        this.getSubjects()
    },
    watch: {
        $route: [
            {
                handler: 'getSubjects',
                immediate: false,
                deep: false
            }
        ],
    },
    methods: {
        getSubjects: function () {
            this.$store.dispatch('getStudentHome')
                .then(response => {
                    this.username = response.data.username
                    this.subjects = response.data.subjects
                })
                .catch(error => {console.log(error)})
        }
    }
}
</script>


