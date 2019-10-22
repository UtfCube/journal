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

              <CheckpointInfo v-for="(date, j) in dates[checkpoint.name]" :key="j" v-model="date" property="date" btype="date" size="is-small"/>  
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
      </table>
    
    <!--<b-table :data="checkpoints" :columns="checkpoints">-->
      
      <!--<template slot-scope="props" slot="header">
        <div style="color: red">{{ props.column.fields }}</div>
        <b-icon
          v-if="props.column.meta"
          pack="fas"
          icon="info-circle"
          size="is-small">
        </b-icon>
      </template>
      -->
      <!--<template slot-scope="props">
        <b-table-column class="vertical-text" v-for="(element, index) in props.row.fields"
            :key="index"
            :label="element.name">
        </b-table-column>
      </template>
    </b-table>-->
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