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
        <section>
            <b-table 
                :data="info"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable
                paginated
                per-page="5"
                >
                <template slot-scope="props">
                    <b-table-column label="Имя преподавателя">
                        {{ props.row.lastname + ' ' + props.row.firstname + ' ' + props.row.patronymic }}
                    </b-table-column>

                    <b-table-column label="Предметы">
                        <ul>
                            <li v-for="(subject, index) in props.row.subjects"
                                :key="index">
                            {{ subject }}
                            </li>
                        </ul>
                    </b-table-column>
                </template>
            </b-table>
        </section>
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

    get info() {
        return this.$store.state.userData.info;
    }
    beforeMount () {
        const error = this.$store.dispatch('getStudentHome');
    }

    click(subject: any) {
        this.$router.push({ name: 'progress', params: { subject: subject}})
    }
}
</script>

