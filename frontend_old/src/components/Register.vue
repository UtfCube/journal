<template>  
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Регистрация</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="control">
            <button class="button is-large is-primary"
            v-for="(component, tab) in tabs"
            :key="tab"
            @click="currentTab = tab"
            >{{ tab }}</button>
        </div>
        <div class="field">
          <label class="label is-large" for="lastname">Фамилия:</label>
          <div class="control">
            <input type="text" class="input is-large" id="lastname" v-model="form.lastname">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="firstname">Имя:</label>
          <div class="control">
            <input type="text" class="input is-large" id="firstname" v-model="form.firstname">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="patronymic">Отчество:</label>
          <div class="control">
            <input type="text" class="input is-large" id="patronymic" v-model="form.patronymic">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="rank">Воинское звание:</label>
          <div class="control">
            <input type="text" class="input is-large" id="rank" v-model="form.rank">
          </div>
        </div>
        <component v-model="form"
            :is="currentTabComponent"
        ></component>
        <div class="field">
          <label class="label is-large" for="username">Имя пользователя:</label>
          <div class="control">
            <input type="text" class="input is-large" id="username" v-model="form.username">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="password">Пароль:</label>
          <div class="control">
            <input type="password" class="input is-large" id="password" v-model="form.password">
          </div>
        </div>
        <div class="field">
          <label class="label is-large" for="mirror_password">Повторите пароль:</label>
          <div class="control">
            <input type="password" class="input is-large" id="mirror_password" v-model="mirror_password">
          </div>
        </div>
        <div class="control">
          <a class="button is-large is-primary" @click="register">Зарегестрироваться</a>
        </div>

      </div>
    </section>
  </div>  
</template>

<script>
import { EventBus } from '@/utils'
import RtfInfo from '@/components/RegisterTutorFormInfo'
import RsfInfo from '@/components/RegisterStudentFormInfo'

export default {
    name: 'register',
    components: { RtfInfo, RsfInfo },
    data: function () {
        return {
            form: {},
            mirror_password: '',
            currentTab: 'Учитель',
            tabs: {
                'Учитель': ['rtf-info', 'tutor'], 
                'Слушатель': ['rsf-info', 'student']
            },
            errorMsg: '',
        }
    },
    computed: {
        currentTabComponent: function () {
            return this.tabs[this.currentTab][0]
        },
        currentType: function () {
            return this.tabs[this.currentTab][1]
        }
    },
    mounted () {
        EventBus.$on('failedRegistering', (msg) => {
        this.errorMsg = msg
        })
    },
    beforeDestroy () {
        EventBus.$off('failedRegistering')
    },
    methods: {
        register () {
            this.$store.dispatch('register', { type: this.currentType, form: this.form })
                .then(() => {
                    console.log('push ' +`/${this.currentType}/home`)
                    this.$router.push(`/${this.currentType}/home`)})
        }
    }
}
</script>

