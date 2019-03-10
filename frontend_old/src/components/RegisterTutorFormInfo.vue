<template>
  <div class="field">
    <label class="label is-large" for="degree">Ученая степень:</label>
    <div class="control">
      <input type="text" class="input is-large" id="degree" :value="value.degree" @input="update('degree', $event.target.value)">
    </div>
  </div>
</template>

<script>
export default {
  props: ['value'],
  methods: {
      update(key, value) {
          this.$emit('input', { ...this.value, [key]: value });
      }
  }
}
</script>


<style>

</style>