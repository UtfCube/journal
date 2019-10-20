<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Здравствуйте, {{ username }}</h2>
                </div>
            </div>
        </section>
        <section>
            <b-table 
                :data="subjects"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable
                paginated
                per-page="5"
                detailed
                >
                <template slot-scope="props">
                    <b-table-column label="Предмет">
                       {{ props.row }}
                    </b-table-column>
                </template>
            </b-table>
        </section>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { DialogError } from '@/utils';

@Component
export default class StudentHome extends Vue {
    private selected: object = {};

    get username() {
        return this.$store.state.userData.username;
    }

    get subjects() {
        return this.$store.state.userData.info;
    }

    async beforeCreate () {
        const error = await this.$store.dispatch('getStudentHome');
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    click(subject: any) {
        this.$router.push({ name: 'progress', params: { subject: subject}})
    }
}
</script>

