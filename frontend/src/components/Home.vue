<template>
    <TutorHome v-if="role=='tutor'"/>
    <StudentHome v-else-if="role=='student'"/>
    <AdminHome v-else-if="role=='admin'"/>
</template>>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';
import TutorHome from '@/components/TutorHome.vue'
import StudentHome from '@/components/StudentHome.vue'
import AdminHome from '@/components/AdminHome.vue'

@Component({
    components: {TutorHome, StudentHome, AdminHome}
})
export default class Home extends Vue {
    get role() {
        return this.$store.state.userData.role
    }
}
</script>>