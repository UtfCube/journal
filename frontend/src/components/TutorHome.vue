<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Здравствуйте, {{ username }}</h2>
                </div>
            </div>
        </section>
        <section class="section">
            <div class="container">
                <b-field label="Предмет:">
                    <b-select v-model="subject" placeholder="Выберете предмет">
                        <option
                            v-for="(subject, index) in subjects"
                            :key="index">
                            {{ subject.name }}
                        </option>
                    </b-select>
                </b-field>
                <b-field label="Группа:">
                    <b-select v-model="group" placeholder="Выберете группу">
                        <option
                            v-for="(group, index) in groups"
                            :key="index">
                            {{ group.id }}
                        </option>
                    </b-select>
                </b-field>
                <div class="control">
                    <a class="button is-primary" @click="add">Добавить</a>
                </div>
                <b-field label="Сменить пароль:">
                    <b-input v-model="new_password"/>
                </b-field>
                <div class="control">
                    <a class="button is-primary" @click="changePassword">Сменить пароль</a>
                </div>
            </div>
        </section>
        <section>
            <b-table 
                :data="assosiations"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable
                @click="click">
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

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';

@Component
export default class TutorHome extends Vue {
    private subject: string = "";
    private group: number = 0;
    private selected: object = {};
    private new_password: string = "";

    async beforeCreate () {
        const error = await this.$store.dispatch('getTutorHome');
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    get username () {
        return this.$store.state.userData.username;
    }

    get assosiations () {
        return this.$store.state.userData.info;
    }

    get groups () {
        return this.$store.state.groups
    }

    get subjects () {
        return this.$store.state.subjects
    }

    async add () {
        const error = await this.$store.dispatch('addAssociation', { group_id: this.group, subject_name: this.subject });
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    click(row: any) {
        console.log(row)
        this.$router.push({name: 'GroupSubject', params: row });
    }

    async changePassword() {
        const error = await this.$store.dispatch('changePassword', { new_password: this.new_password});
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }
}
</script>

