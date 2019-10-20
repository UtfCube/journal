<template>
    <div>
        <section class="hero is-primary">
                <div class="hero-body">
                    <div class="container has-text-centered">
                        <h2 class="title">Здравствуйте, {{ username }}</h2>
                    </div>
                </div>
        </section>
        <section>
            <b-field label="Слушатели:">
                <b-upload v-model="studentFile"
                    drag-drop>
                    <section class="section">
                        <div class="content has-text-centered">
                            <p>Drop your files here or click to upload</p>
                        </div>
                    </section>
                </b-upload>
                <div class="tags">
                    <span class="tag is-primary" v-if="studentFile">
                        {{studentFile.name}}
                        <button class="delete is-small"
                            type="button"
                            @click="deleteStudentFile">
                        </button>
                    </span>
                </div>
            </b-field>
        </section>

        <section>
            <b-field label="Преподаватели:">
                <b-upload v-model="tutorFile"
                    drag-drop>
                    <section class="section">
                        <div class="content has-text-centered">
                            <p>Drop your files here or click to upload</p>
                        </div>
                    </section>
                </b-upload>
                <div class="tags">
                    <span class="tag is-primary" v-if="tutorFile">
                        {{tutorFile.name}}
                        <button class="delete is-small"
                            type="button"
                            @click="deleteTutorFile">
                        </button>
                    </span>
                </div>
            </b-field>
        </section>
        <section>
            <b-field label="Предметы:">
                <b-upload v-model="subjectFiles"
                    multiple
                    drag-drop>
                    <section class="section">
                        <div class="content has-text-centered">
                            <p>Drop your files here or click to upload</p>
                        </div>
                    </section>
                </b-upload>
            </b-field>

            <div class="tags">
                <span v-for="(file, index) in subjectFiles"
                    :key="index"
                    class="tag is-primary" >
                    {{file.name}}
                    <button class="delete is-small"
                        type="button"
                        @click="deleteSubjectFile(index)">
                    </button>
                </span>
            </div>

            <div class="control">
                    <a class="button is-primary" @click="add">Загрузить</a>
                </div>
        </section>
    </div>
</template>>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { DialogError } from '@/utils';

@Component
export default class AdminHome extends Vue {
    private studentFile: File | null = null;
    private tutorFile: File | null = null;
    private subjectFiles: any[] = [];

    get username () {
        return this.$store.state.userData.username;
    }

    deleteSubjectFile(index: number) {
        this.subjectFiles.splice(index, 1)
    }

    deleteStudentFile() {
        this.studentFile = null;
    }

    deleteTutorFile() {
        this.tutorFile = null;
    }

    async add() {
        let formData = new FormData();
        if (this.studentFile)
            formData.append('students', this.studentFile);
        if (this.tutorFile)
            formData.append('tutors', this.tutorFile);
        for (let key in this.subjectFiles) {
            formData.append(`subject${key}`, this.subjectFiles[key]);
        }
        const error = await this.$store.dispatch('AdminUpload', formData);
        if (error) {
            this.$dialog.alert({ ...DialogError, message: error });
        }
    }
}
</script>>