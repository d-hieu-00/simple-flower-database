<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>

<template>
    <div class="container pl-5" style="height: inherit;">
        <img alt="Monitor logo" class="logo" src="@/assets/logo.jpg" width="150" height="150" />
        <div class="container">
            <div class="row" style="margin-top: 20px;">
                <RouterLink class="col btn card shadow" style="margin-right: 5px;" to="/">Homne</RouterLink>
                <RouterLink class="col btn card shadow" style="margin-left: 5px;" to="/about">About</RouterLink>
            </div>
        </div>
        <div class="card shadow" style="margin-top: 10px;">
            <div class="card-body">
                <p class="fw-semibold">Flower database</p>
                <ul>
                    <li>Nguyễn Duy Hiệu</li>
                    <li>Nguyễn Thị Kim Yến</li>
                </ul>
            </div>
        </div>
        <div class="card shadow" style="margin-top: 20px;">
            <div class="card-body">
                <p v-show="searching === true">
                    Searching flower
                    <font-awesome-icon class="fa-spin" icon="fa-solid fa-spinner" />
                </p>
                <div v-show="searching === false">
                    <!-- <p>Total images found: <b>{{ displayText.count }}</b></p> -->
                    <p>Time DB query: <b>{{ displayText.db_time }}</b> in millisecond</p>
                    <p>Time extract features: <b>{{ displayText.ext_time }}</b> in millisecond</p>
                </div>
            </div>
        </div>
        <div class="card shadow" style="margin-top: 20px;" v-show="loadedFile">
            <img class="image-item card-img-top" :src="fileURL" style="max-height: 300px;">
            <div class="card-body d-flex justify-content-center">
                <button :disabled="handling || searching !== false || displayText.count <= 0" class="btn btn-success" @click="addImage">
                    Add this image to database
                </button>
            </div>
        </div>
    </div>
    <div class="pt-3 pb-3" style="height: 100%;">
        <RouterView @fileChanged="onFileChanged" @searchResult="onSearchResult"/>
    </div>
</template>

<style scoped>
.logo {
    display: block;
    margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
    .logo {
        margin: 0 2rem 0 0;
    }

    nav {
        text-align: left;
        margin-left: -1rem;
        font-size: 1rem;

        padding: 1rem 0;
        margin-top: 1rem;
    }
}
</style>

<script lang="ts">
import { ref } from 'vue'
import { toast } from 'vue3-toastify';

export default {
    components: {},
    data() {
        return {
            loadedFile: ref(false),
            fileInfo: ref(null),
            fileURL: ref(""),
            searching: ref(false),
            handling: ref(false),
            displayText: ref({
                count: 0,
                db_time: 0,
                ext_time: 0,
            } as any),
        }
    },
    methods: {
        onFileChanged(file: any) {
            if (file) {
                this.readFile(file);
                this.loadedFile = true;
                this.fileInfo = file;
            } else {
                this.loadedFile = false;
                this.fileInfo = null;
            }
        },
        onSearchResult(info: any) {
            this.searching = info.searching;
            if (typeof info.count === typeof 1) {
                this.displayText.count = info.count;
            }
            if (typeof info.db_time === typeof 1) {
                this.displayText.db_time = info.db_time;
            }
            if (typeof info.ext_time === typeof 1) {
                this.displayText.ext_time = info.ext_time;
            }
            console.log(info);
        },
        readFile(file: any) {
            const reader = new FileReader();
            reader.onload = (e: any) => {
                // Update the fileURL with the data URL of the uploaded file
                this.fileURL = e.target.result;
            };
            reader.readAsDataURL(file);
        },
        addImage() {
            if (!this.fileInfo) {
                toast.error("Something went wrong!");
                return;
            }
            let url = `${location.toString()}api/image`;
            fetch(url, { method: "POST", body: this.fileInfo }).then((response) => {
                return response.json();
            }).then((data) => {
                if (data["error"]) {
                    toast.error(data["error"], { autoClose: 2000 });
                    return;
                }
                toast.success("Add image successfully", { autoClose: 2000 });
            }).catch(err => {
                toast.error(err);
            }).finally(() => {
                this.$emit("reloadImage");
                // this.$refs.childComponent.doSearchString();
            });
        }
    },
}
</script>