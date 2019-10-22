<template>
    <div>

    <b-table :data="checkpoints" :columns="checkpoints">
      
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
      <template slot-scope="props">
        <b-table-column class="vertical-text" v-for="(element, index) in props.row.fields"
            :key="index"
            :label="element.name">
        </b-table-column>
      </template>
    </b-table>
    </div>
</template>>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';

@Component
export default class GroupSubject extends Vue {
    private newProgress: any = {};
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

    get checkpoints() {
        return this.$store.state.currentCheckpoints
    }
}
</script>