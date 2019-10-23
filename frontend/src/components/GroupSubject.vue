<template>
    <div>
      <table class="table table-header-rotated">
        <thead>
          <tr>
            <th>
              fullname
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
            <th class="rotate" v-for="(field, j) in fields"
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
          <tr v-for="(userInfo, i) in progress" :key="i">
            <td>
              <span>{{userInfo.fullname}}</span>
            </td>  
            <td v-for="(p, j) in userInfo.progress" :key="j">
              <CheckpointInfo v-if="p.type=='5'" v-model="userInfo.progress[j]" property="result" btype="number" min="1" max="5" size="is-small"/>
              <span v-else-if="p.type=='+'" @click="change(p)">{{ p.result }}</span>
              <CheckpointInfo v-else-if="p.type=='d'" v-model="userInfo.progress[j]" property="result" btype="date" size="is-small"/>
              <CheckpointInfo v-else v-model="userInfo.progress[j]" property="result" btype="text" size="is-small"/>
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
    private newProgress: any = {};
    private newDates: any = {};
    private cp_name: string = "";
    private newCheckpoints: any[] = [];
    private selected: any = {};
    private edit: boolean = false;
    private symbols: any = ["-", "+/-", "+", "*"]
    private dates_names:  any = ["Дата проведения", "Льготный срок сдачи", "Крайний срок сдачи"]
    private znak: string = ""

    
    async beforeMount() {
        let error = await this.$store.dispatch('getCheckpoints', {subject_name: this.$route.params.subject_name});
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
        error = await this.$store.dispatch('getGradesTable', this.$route.params);
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }

    getFieldsLength(checkpoint: any) {
      let length = checkpoint.fields.length
      return checkpoint.fields.length
    }

    get checkpoints() {
        return this.$store.state.currentCheckpoints
    }

    get fields() {
      return this.$store.getters.getFields
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

    async save(cp_name: string, info: any) {
      let i = this.dates_names.indexOf(info['name'])
      if (i != -1) {
        let left = 0;
        let right = 0;
      }
      //this.newDates = {...this.newDates, [cp_name]: info}
      const error = await this.$store.dispatch('addDates', { ...this.$route.params, dates: {[cp_name]: [info]}});
      if (error) {
          this.$dialog.alert({ ...DialogError, message: error });
      }
    }

    change(p: any) {
      let i = this.symbols.indexOf(p.result)
      if (i == -1) {
        p.result = '+/-'
      }
      else {
        i = (i + 1) % this.symbols.length
        p.result = this.symbols[i]
      }
      console.log(p)
    }
}
</script>

<style lang='scss' scoped>
.table-header-rotated {
  border-collapse: collapse;
  td {
    width: 20px;
  }
  th {
    border-bottom: 1px solid rgb(0, 0, 0);
    border-top: 1px solid rgb(0, 0, 0);
    border-left: 1px solid rgb(0, 0, 0);
    border-right: 1px solid rgb(0, 0, 0);
    padding: 10px 10px;
    text-align: center;
  }
  td {
    text-align: center;
    padding: 10px 5px;
    border: 1px solid rgb(0, 0, 0);
  }
  th.rotate {
    height: 195px;
    white-space: nowrap;
    // Firefox needs the extra DIV for some reason, otherwise the text disappears if you rotate 
    > div {
      transform: 
        // Magic Numbers
        translate(0px, 160px)
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