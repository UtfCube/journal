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
          <tr>
            <td/>  
            <td v-for="(field, j) in fields" :key="j">
              <CheckpointInfo v-if="field.type=='5'" v-model="selected" property="date" btype="number" min="2" max="5" size="is-small"/>
              <CheckpointInfo v-else-if="field.type=='+'" v-model="selected" property="date" btype="text" size="is-small"/>
              <CheckpointInfo v-else-if="field.type=='d'" v-model="selected" property="date" btype="date" size="is-small"/>
              <CheckpointInfo v-else v-model="selected" property="date" btype="text" size="is-small"/>
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

    
    async beforeMount() {
        console.log(this.$route.params)
        let error = await this.$store.dispatch('getCheckpoints', {subject_name: this.$route.params.subject_name});
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
        //error = await this.$store.dispatch('getGradesTable', this.$route.params);
        //if (error) {
        //    this.$dialog.alert({ ...DialogError, message: error });
        //}
    }

    getFieldsLength(checkpoint: any) {
      let length = checkpoint.fields.length
      return checkpoint.fields.length
    }

    get checkpoints() {
        return this.$store.state.currentCheckpoints
    }

    get fields() {
      let fields = []
      for (let checkpoint of this.$store.state.currentCheckpoints) {
        fields.push(...checkpoint.fields)
      }
      return fields
    }

    get dates() {
      for (let checkpoint of this.$store.state.currentCheckpoints) {
        this.newDates[checkpoint.name] = checkpoint.dates
      }
      return this.newDates
    }

    async save(cp_name: string, info: any) {
      this.newDates = {...this.newDates, [cp_name]: info}
      const error = await this.$store.dispatch('addDates', { ...this.$route.params, dates: {[cp_name]: [info]}});
      if (error) {
          this.$dialog.alert({ ...DialogError, message: error });
      }
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