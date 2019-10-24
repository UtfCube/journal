<template>
    <b-input v-if="btype!='number'"
        :type="btype"
        :value="value[property]"
        :size="size"
        @input="update(property, $event)"
    >
    </b-input>
    <b-input v-else
        :type="btype"
        :value="value[property]"
        :size="size"
        :min="min"
        :max="max"
        @input="update(property, $event)"
    >
    </b-input>
</template>


<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';

@Component
export default class CheckpointInfo extends Vue {
  @Prop({
    type: Object,
  })
  private value: any;
  
  @Prop({
    type: String,
  })
  private property!: string;
  
  @Prop({
    type: String,
  })
  private btype!: string;

  @Prop({
    type: String,
  })
  private size!: string;

  @Prop({
    type: String,
  })
  private min!: number;
  
  @Prop({
    type: String,
  })
  private max!: number;

  private localDate: string = '';

  update(key: any, value: any) {
    this.$emit('input', { ...this.value, [key]: value });
  }
}
</script>