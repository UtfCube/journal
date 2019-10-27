<template>
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


<style>

</style>