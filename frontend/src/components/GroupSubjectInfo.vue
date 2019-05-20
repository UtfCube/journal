<template>
    <div>
        <section class="hero is-primary">
            <div class="hero-body">
                <div class="container has-text-centered">
                    <h2 class="title">Контрольные точки</h2>
                    <p class="subtitle">По предмету {{ $route.params.subject_name }} группы {{ $route.params.group_id }}</p>
                    <p v-if="error" class="subtitle error-msg">{{ error }}</p>
                </div>
            </div>
        </section>
        <div class="field">
          <label class="label" for="name">Название:</label>
          <div class="control">
            <input type="text" class="input" id="name" v-model="cp_name">
          </div>
        </div>
        <div class="field" v-for="id in ids" :key="id">
          <label class="label" for="name">Поле:</label>
          <div class="control">
            <input type="text" class="input" id="name" v-model="cp_fields[id - 1]">
          </div>
        </div>
        <!--
        <b-field label="Дата сдачи:">
            <b-datepicker v-model="checkpoint.posting_date"
                :first-day-of-week="1"
                placeholder="Нажмите для выбора...">

                <button class="button is-primary"
                    @click="checkpoint.posting_date = new Date()">
                    <b-icon icon="calendar-today"></b-icon>
                    <span>Сегодня</span>
                </button>

        </b-field>
        <b-field label="Крайняя дата сдачи:">
            <b-datepicker v-model="checkpoint.critical_date"
                :first-day-of-week="1"
                placeholder="Нажмите для выбора...">

                <button class="button is-primary"
                    @click="checkpoint.critical_date = new Date()">
                    <b-icon icon="calendar-today"></b-icon>
                    <span>Сегодня</span>
                </button>

                <button class="button is-danger"
                    @click="checkpoint.critical_date = null">
                    <b-icon icon="close"></b-icon>
                    <span>Очистить</span>
                </button>
            </b-datepicker>
        </b-field>
        -->
        <div class="control">
          <a class="button is-primary" @click="addField">Добавить поле</a>
        </div>
        <div class="control">
          <a class="button is-primary" @click="addCheckpoint">Добавить контрольную точку</a>
        </div>
        <section>
            <b-table
                :data="newCheckpoints">
                <template slot-scope="props">
                    <b-table-column field="name" label="Название">
                        {{ props.row.name }}
                    </b-table-column>

                    <b-table-column field="fields" label="Поля">
                        <ul>
                            <li v-for="(field, index) in props.row.fields"
                                :key="index">
                            {{ field }}
                            </li>
                        </ul>
                    </b-table-column>
                </template>
            </b-table>
        </section>
        <div class="control">
          <a class="button is-primary" @click="saveCheckpoints">Сохранить контрольные точки</a>
        </div>
        <section>
            <b-table 
                :data="checkpoints"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable
                paginated
                per-page="5"
                detailed
                @details-open="(row, index) => $store.dispatch('getProgress', { ...this.$route.params, checkpoint_name: row.name })"
                >
                <template slot-scope="props">
                    <b-table-column field="name" label="Название">
                        {{ props.row.name }}
                    </b-table-column>

                    <b-table-column field="fields" label="Поля">
                        <ul>
                            <li v-for="(field, index) in props.row.fields"
                                :key="index">
                            {{ field }}
                            </li>
                        </ul>
                    </b-table-column>
                </template>
                <template slot="detail" slot-scope="details">
                    <b-table :data="getProgressByCheckpoint(details.row.name)"
                        :hoverable="true" 
                        :striped="true">
                        <template slot-scope="props">
                            <b-table-column label="Имя">
                                {{ props.row.lastname + ' ' + props.row.firstname + ' ' + props.row.patronymic }}
                            </b-table-column>

                            <b-table-column v-for="(value, key, index) in props.row.progress"
                                :key="index"
                                :label="key">
                                {{ value }}
                            </b-table-column>
                        </template>
                    </b-table>
                </template>
            </b-table>
        </section>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class GroupSubjectInfo extends Vue {
    private error: string = '';
    private checkpoint: any = {
        "name": "",
        "fields": []
    };
    private cp_name: string = "";
    private cp_fields: any = {};
    private newCheckpoints: any[] = [];
    private selected: any = {};
    private ids: number[] = [];
    
    async beforeMount() {
        this.error = await this.$store.dispatch('getCheckpoints', this.$route.params);
    }

    get checkpoints() {
        return this.$store.state.currentCheckpoints;
    }

    getProgressByCheckpoint(checkpoint: string) {
        return this.$store.state.progress[checkpoint]
    }

    addCheckpoint() {
        this.newCheckpoints.push({ name: this.cp_name, fields: Object.values(this.cp_fields)})
    }

    async saveCheckpoints() {
        this.error = await this.$store.dispatch('addCheckpoints', { ...this.$route.params, checkpoints: this.newCheckpoints });
    }

    addField() {
        this.ids.push(this.ids.length + 1);
    }
}
</script>
