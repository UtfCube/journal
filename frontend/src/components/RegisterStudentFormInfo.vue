<template>
  <div class="field">
    <label class="label is-small" for="fullname">Fullname:</label>
    <div class="control">
      <input type="text" class="input is-small" id="fullname" :value="value.fullname" @input="update('fullname', $event.target.value)">
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class RsfInfo extends Vue {
    @Prop({
        type: Object
    })
    private value: any;

    update(key: any, value: any) {
        this.$emit('input', { ...this.value, [key]: value });
    }
}
</script>

