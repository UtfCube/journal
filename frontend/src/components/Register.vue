<template>  
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Регистрация</h2>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="control">
            <button class="button is-small is-primary"
            v-for="(component, tab) in tabs"
            :key="tab"
            @click="currentTab = tab"
            >{{ tab }}</button>
        </div>
        <div class="field">
          <label class="label is-small" for="lastname">ФИО:</label>
          <div class="control">
            <input type="text" class="input is-small" id="lastname" v-model="form.fio">
          </div>
        </div>
        <component v-model="form"
            :is="currentTabComponent"
        ></component>
        <div class="field">
          <label class="label is-small" for="username">Имя пользователя:</label>
          <div class="control">
            <input type="text" class="input is-small" id="username" v-model="form.username">
          </div>
        </div>
        <div class="field">
          <label class="label is-small" for="password">Пароль:</label>
          <div class="control">
            <input type="password" class="input is-small" id="password" v-model="form.password">
          </div>
        </div>
        <div class="field">
          <label class="label is-small" for="mirror_password">Повторите пароль:</label>
          <div class="control">
            <input type="password" class="input is-small" id="mirror_password" v-model="mirror_password">
          </div>
        </div>
        <div class="control">
          <a class="button is-small is-primary" @click="register">Зарегистрироваться</a>
        </div>

      </div>
    </section>
  </div>  
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';
import RtfInfo from '@/components/RegisterTutorFormInfo.vue';
import RsfInfo from '@/components/RegisterStudentFormInfo.vue';

@Component({
  components: {RtfInfo, RsfInfo}
})
export default class Register extends Vue {
  private form: any = {};
  private mirror_password: string = '';
  private currentTab: string = 'Учитель';
  private tabs: any = {
    'Учитель': ['RtfInfo', 'tutor'], 
    'Слушатель': ['RsfInfo', 'student']
  };
  private errorMsg: string = '';

  get currentTabComponent () {
    return this.tabs[this.currentTab][0]
  }

  get currentType() {
    return this.tabs[this.currentTab][1]
  }

  async register () {
    const error = await this.$store.dispatch('register', { role: this.currentType, ...this.form })
    if (error) {
        this.$dialog.alert({ ...DialogError, message: error });
      }   
    else {
      this.$router.push(`/home`);
    }
  }
}
</script>