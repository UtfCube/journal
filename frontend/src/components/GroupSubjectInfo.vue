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
          <label class="label is-medium" for="name">Название:</label>
          <div class="control">
            <input type="text" class="input is-medium" id="name" v-model="checkpoint.name">
          </div>
        </div>
        <b-field label="Дата сдачи:">
            <b-datepicker v-model="checkpoint.posting_date"
                :first-day-of-week="1"
                placeholder="Нажмите для выбора...">

                <button class="button is-primary"
                    @click="checkpoint.posting_date = new Date()">
                    <b-icon icon="calendar-today"></b-icon>
                    <span>Сегодня</span>
                </button>

                <button class="button is-danger"
                    @click="checkpoint.posting_date = null">
                    <b-icon icon="close"></b-icon>
                    <span>Очистить</span>
                </button>
            </b-datepicker>
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
        <!--<div class="field">
          <label class="label is-medium" for="posting_date">Дата сдачи:</label>
          <div class="control">
            <input type="date" class="input is-medium" id="posting_date" v-model="checkpoint.posting_date">
          </div>
        </div>
        <div class="field">
          <label class="label is-medium" for="critical_date">Крайняя дата сдачи:</label>
          <div class="control">
            <input type="date" class="input is-medium" id="critical_date" v-model="checkpoint.critical_date">
          </div>
        </div>
        -->
        <div class="control">
          <a class="button is-medium is-primary" @click="addCheckPoint">Добавить</a>
        </div>

        <section>
            <b-table 
                :data="checkpoints"
                :selected.sync="selected" 
                :hoverable="true" 
                :striped="true"
                focusable>
                <template slot-scope="props">
                    <b-table-column field="name" label="Название">
                        {{ props.row.name }}
                    </b-table-column>

                    <b-table-column field="posting_date" label="Дата сдачи" centered>
                        {{ new Date(props.row.posting_date).toLocaleDateString() }}
                    </b-table-column>

                    <b-table-column field="critical_date" label="Крайняя дата сдачи" centered>
                        {{ new Date(props.row.critical_date).toLocaleDateString() }}
                    </b-table-column>
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
    private checkpoint: any = {};
    private selected: any = {};
    
    beforeMount() {
        this.$store.dispatch('getCheckPoints', this.$route.params);
    }

    get checkpoints() {
        return this.$store.state.currentCheckpoints;
    }

    addCheckPoint() {
        this.$store.dispatch('addCheckPoint', { ...this.$route.params, checkpoint: this.checkpoint });
    }
}
</script>
