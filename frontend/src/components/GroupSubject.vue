<template>
    <div>
      <table v-if="role=='tutor'" class="table table-header-rotated">
        <thead>
          <tr>
            <th>
              fullname
            </th>
            <th>
              ФИО
            </th>
            <th v-for="(checkpoint, i) in checkpoints"
              :key="i" :colspan="checkpoint.fields.length">
              {{ checkpoint.name }}
              <b-field v-for="(date, j) in dates[checkpoint.name]" :key="j" :label="date.name" label-position="on-border">
                <CheckpointInfo  :value="dates[checkpoint.name][j]" @input="save(checkpoint.name, $event)" property="date" btype="date" size="is-small"/>  
              </b-field>
            </th>
          </tr>
          <tr>
            <th/>
            <th/>
            <th class="rotate" v-for="(field, j) in fields"
                :key=j>
                <div>
                  <span v-if="field.name=='Оценка'" @click="sort(field.cp_name)">
                    {{ field.name }}
                  </span>
                  <span v-else>
                    {{ field.name }}
                  </span>
                </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(userInfo, i) in progress" :key="i">
            <td>
              <span>{{userInfo.fullname}}</span>
            </td>
            <td>
              <span>{{userInfo.fio}}</span>
            </td>  
            <td v-for="(p, j) in userInfo.progress" :style="getColor(userInfo.fio, userInfo.progress, p)" :key="j">
              <span v-if="p.type=='+'" @click="saveCell(userInfo.username, change(p))">{{ p.result ? p.result: "-"  }}</span>
              <CheckpointInfo v-else-if="p.type=='5'" :value="userInfo.progress[j]" @input="saveCell(userInfo.username, $event)" property="result" btype="number" min="1" max="5" size="is-small"/>
              <CheckpointInfo v-else-if="p.type=='n'" :value="userInfo.progress[j]" @input="saveCell(userInfo.username, $event)" property="result" btype="number" min="0" size="is-small"/>
              <CheckpointInfo v-else-if="p.type=='d'" :value="userInfo.progress[j]" @input="saveCell(userInfo.username, $event)" property="result" btype="date" size="is-small"/>
              <b-select v-else-if="p.type=='p'" :value="p.result" @input="saveTutor(userInfo.username, p, $event)" placeholder="Преподаватель">
                <option
                    v-for="(tutor, id) in tutors"
                    :key="id">
                    {{ tutor.fio }}
                </option>
              </b-select>
              <CheckpointInfo v-else :value="userInfo.progress[j]" property="result" @input="saveCell(userInfo.username, $event)" btype="text" size="is-small"/>
            </td> 
          </tr>
        </tbody>
      </table>
      <table v-else-if="role=='student'" class="table table-header-rotated">
        <thead>
          <tr>
            <th>
              fullname
            </th>
            <th v-for="(checkpoint, i) in checkpoints_s"
              :key="i" :colspan="checkpoint.fields.length">
              {{ checkpoint.name }}
              <b-field v-for="(date, j) in dates[checkpoint.name]" :key="j" :label="date.name" label-position="on-border">
                <span>{{date.date}}</span>
              </b-field>
            </th>
          </tr>
          <tr>
            <th/>
            <th class="rotate" v-for="(field, j) in fields_s"
                :key=j>
                <div>
                  <span>
                    {{ field.name }}
                  </span>
                </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(userInfo, i) in progress_s" :key="i" :style="username === userInfo.username ? 'background-color:#ACACAC' : undefined ">
            <td>
              <span>{{userInfo.fullname}}</span>
            </td>  
            <td v-for="(p, j) in userInfo.progress" :style="getColor(userInfo.fio, userInfo.progress, p)" :key="j">
              <span>{{ p.result }}</span>
            </td> 
          </tr>
        </tbody>
      </table>
    </div>
</template>>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';
import CheckpointInfo from './CheckpointInfo.vue';

@Component({
    components: {CheckpointInfo}
})
export default class GroupSubject extends Vue {
    private newDates: any = {};
    private selected: any = {};
    private edit: boolean = false;
    private symbols: any = ["-", "+/-", "+", "*"]
    private dates_names:  any = ["Дата проведения", "Льготный срок сдачи", "Крайний срок сдачи"]

    
    async beforeMount() {
        let error = await this.$store.dispatch('getCheckpoints', {subject_name: this.$route.params.subject_name});
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
        error = await this.$store.dispatch('getGradesTable', this.$route.params);
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
        error = await this.$store.dispatch('getTutors');
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    getFieldsLength(checkpoint: any) {
      let length = checkpoint.fields.length
      return checkpoint.fields.length
    }

    sort(cp_name: string) {
      this.$store.commit('sortGradeTable', {cp_name: cp_name});
    }

    get checkpoints() {
        return this.$store.state.currentCheckpoints
    }

    get fields() {
      return this.$store.getters.getFields
    }

    get checkpoints_s() {
      let c = []
      for (let checkpoint of this.$store.state.currentCheckpoints) {
        c.push({
          "name": checkpoint.name,
          "fields": checkpoint.fields.filter((x:any) => x.is_hidden === false)
        })
      }
      return c
      //this.$store.state.currentCheckpoints
    }

    get fields_s() {
      return this.$store.getters.getFields.filter((x:any) => x.is_hidden === false)
    }

    get tutors() {
      return this.$store.state.tutors
    }

    get dates() {
      for (let checkpoint of this.$store.state.currentCheckpoints) {
        this.newDates[checkpoint.name] = checkpoint.dates
      }
      return this.newDates
    }

    get progress() {
      return this.$store.getters.getProgress
    }

    get progress_s() {
      let p:any = []
      for (let pr of this.$store.getters.getProgress) {
        p.push({
          username: pr.username,
          fio: pr.fio,
          fullname: pr.fullname,
          progress: pr.progress.filter((x: any)=> x.is_hidden === false)
        })
      }
      return p
    }

    get role() {
      return this.$store.state.userData.role
    }

    async save(cp_name: string, info: any) {
      const error = await this.$store.dispatch('addDates', { ...this.$route.params, dates: {[cp_name]: [info]}});
      if (error) {
          this.$dialog.alert({ ...DialogError, message: error });
      }
    }

    checkDates(cp_name:string, date: string) {
      let dates = this.dates[cp_name]
      for (let date of dates) {
        if (date.date === "") {
          return 'background-color:#FFFFFF';
        }
      }
      if (dates[0].date <= dates[1].date && dates[1].date <= dates[2].date) {
        if (date <= dates[1].date)
          return 'background-color:#00FF00'
        if (dates[1].date < date && date <= dates[2].date) {
          return 'background-color:#FFFF00'
        }
        if (dates[2].date <= date) {
          return 'background-color:#FF0000'
        }
      }
      else {
        return 'background-color:#FFFFFF'
      }
    }
    
    getColor(fio:string, user_progress:any, field_progress:any) {
      let dates = this.dates[field_progress.cp_name]
      if (field_progress.name == 'Оценка' && dates.length === 3) {
        let date = user_progress.find((x:any) => x.name === 'Дата сдачи' && x.cp_name == field_progress.cp_name)
        let color = this.checkDates(field_progress.cp_name, date.result)
        return color
      }
    }

    async saveCell(username: string, info: any) {
      let progress = []
      progress.push({
        "username": username,
        "progress": [
          {
            "name": info.cp_name,
            "results": [
              {
                "name": info.name,
                "result": info.result
              }
            ]
          }
        ]
      })
      let cp = this.checkpoints.find((x:any) => x.name == info.cp_name)
      let currentDate = (()=> {
            let now = new Date()
            var mm = now.getMonth() + 1; // getMonth() is zero-based
            var dd = now.getDate();

            return [now.getFullYear(),
                    (mm>9 ? '' : '0') + mm,
                    (dd>9 ? '' : '0') + dd
                  ].join('-');
          })()
      if (cp.fields.length > 1 && info.name == 'Оценка') {
        progress[0].progress[0].results.push({
          name: "Дата сдачи",
          result: currentDate
        })
      }
      const error = await this.$store.dispatch('addProgress', { ...this.$route.params, progress: progress});
      if (error) {
          this.$dialog.alert({ ...DialogError, message: error });
      }
      else {
        if (cp.fields.length > 1 && info.name == 'Оценка') { 
          let color = this.checkDates(cp.name, currentDate)
        }
      }
    }

    async saveTutor(username: string, p: any, tutor:string) {
      let info = JSON.parse(JSON.stringify(p))
      info.result = tutor
      await this.saveCell(username, info)
    }

    change(p: any) {
      let res = JSON.parse(JSON.stringify(p))
      let i = this.symbols.indexOf(res.result)
      if (i == -1) {
        res.result = '+/-'
      }
      else {
        i = (i + 1) % this.symbols.length
        res.result = this.symbols[i]
      }
      return res
    }

    get username() {
      return this.$store.getters.getUsername;
    }
}
</script>

<style lang='scss' scoped>
.table-header-rotated {
  border-collapse: collapse;

  tr:hover td {
    background-color: rgb(172, 172, 172);
  }

  td {
    width: 20px;
    border: 1px solid rgb(0, 0, 0);
  }
  th {
    border-bottom: 1px solid rgb(0, 0, 0);
    border-top: 1px solid rgb(0, 0, 0);
    border-left: 1px solid rgb(0, 0, 0);
    border-right: 1px solid rgb(0, 0, 0);
    padding: 10px 10px;
    text-align: center;
    width: 500px;
  }
  td {
    text-align: center;
    padding: 10px 5px;
    border: 1px solid rgb(0, 0, 0);
  }
  th.rotate {
    height: 250px;
    white-space: nowrap;
    // Firefox needs the extra DIV for some reason, otherwise the text disappears if you rotate 
    > div {
      transform: 
        // Magic Numbers
        translate(0px, 220px)
        // 45 is really 360-45
        rotate(-90deg);
      width: 20px;
    }
    > div > span {
      //border-collapse: collapse;
      //border-bottom: 1px solid rgb(0, 0, 0);
      padding: 5px 10px;
    }
  }
  th.row-header {
    padding: 0 10px;
    border-bottom: 1px solid rgb(0, 0, 0);
  }
}
</style>