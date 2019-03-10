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
        <section class="section">
            <div class="container">
                <div class="field">
                    <label class="label is-large" for="subject">Предмет:</label>
                    <div class="control">
                        <input type="text" class="input is-large" id="subject" v-model="form.subject">
                    </div>
                </div>
                <div class="field">
                    <label class="label is-large" for="group">Группа:</label>
                    <div class="control">
                        <input type="text" class="input is-large" id="group" v-model="form.group">
                    </div>
                </div>
                <div class="control">
                    <a class="button is-large is-primary" @click="add">Добавить</a>
                </div>
            </div>
        </section>
        <section>
            <b-table :data="assosiations" hoverable="true" striped="true">
                <template slot-scope="props">
                    <b-table-column field="group_id" label="Группа" width="80" numeric>
                        {{ props.row.group_id }}
                    </b-table-column>

                    <b-table-column field="subject_name" label="Предмет" >
                        {{ props.row.subject_name }}
                    </b-table-column>
                </template>
            </b-table>
        </section>
    </div>
</template>

<script>
export default {
    name: 'tutor-home',
    data: function () {
        return {
            form: {},
            error: ''
        }
    },
    beforeMount () {
        this.error = this.$store.dispatch('getTutorHome');
    },
    computed: {
        username () {
            return this.$store.state.userData.username;
        },
        assosiations () {
            return this.$store.state.userData.info;
        },
    }
}
</script>
