<template @reloadImage="doSearchString">
    <div class="inherit-height card shadow">
        <div class="card-header">
            <div class="input-group mb-2 mt-2">
                <input type="text" class="form-control" placeholder="Name of flower" v-model="searchString"
                    @keyup.enter="doSearchString">
                <button class="btn btn-outline-secondary" type="button" @click="doSearchString">Search</button>
                <input id="input-file" type="file" accept="image/*" style="display: none" @change="handleFileChange">
                <button class="btn btn-outline-secondary" type="button" @click="openFileInput">Search by image</button>
            </div>
        </div>
        <div class="card-body" id="m-card">
            <div class="scrollable-card">
                <div class="image-grid" :style="{ maxHeight: cardBodyHeight + 'px' }">
                    <div class="card m-0 image-card" v-for="item in loadImages.images" @mouseover="hoverIndex = item.id"
                        @mouseleave="hoverIndex = null">
                        <img class="rounded image-item card-img-top" :src="item.realPath">
                        <button class="delete-button btn btn-warning" @click="deleteImage(item.id)" v-show="hoverIndex === item.id">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-footer d-flex">
            <div class="me-auto p-2"></div>
            <div class="btn-group" role="group">
                <button type="button" class="btn btn-primary dropdown-toggle" :class="displaySizes.class" data-bs-toggle="dropdown">
                    {{ displaySizes.label }}
                </button>
                <ul class="dropdown-menu">
                    <li v-for="opt in displaySizes.options">
                        <a class="dropdown-item" @click="updateDisplaySize(opt)">{{ opt }}</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>
.scrollable-card {
    overflow-y: auto;
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-gap: 10px;
}

.card {
  height: 100%; /* Set a fixed height for all cards */
}

.image-card:hover .delete-button {
  display: block; /* Show delete button when hovering over the card */
}

.delete-button {
  display: none; /* Hide delete button by default */
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const cardBodyHeight = ref(0);
const hoverIndex = ref(null);

onMounted(() => {
    const cardBody = document.querySelector('#m-card');
    if (cardBody) {
        cardBodyHeight.value = cardBody.clientHeight - 50;
    }
});
</script>

<script lang="ts">
import { toast } from 'vue3-toastify';

var backupData = {
    oldSearchString: "",
};

export default {
    components: {},
    data() {
        return {
            searchString: "",
            loadImages: ref({
                count: 0,
                images: []
            } as any),
            loadingImages: ref(false),
            loadingTokens: ref(false),
            loadedTokens: ref(""),
            displaySizes: {
                class: "",
                label: "Display size [30]",
                choose: 30,
                options: [ 10, 15, 20, 30, 50, 70, 100, 200, 300]
            },
        }
    },
    methods: {
        doSearchString() {
            if (this.searchString  === undefined || this.searchString === null || this.searchString === "") {
                toast.warn("Empty string. Please input the name of flower");
                return;
            }

            if (this.loadingImages == true && backupData.oldSearchString == this.searchString) {
                toast.info("Loading images. Please wait!")
            }

            if (this.loadingTokens === false) {
                this.$emit('fileChanged', null);
            }

            let url = `${location.toString()}api/image?query=${this.searchString}&size=${this.displaySizes.choose}`;
            this.$emit("searchResult", { searching: true, count: 0, time: 0 })
            this.loadingImages = true;
            backupData.oldSearchString = this.searchString;
            fetch(url, { method: "GET" }).then((response) => {
                response.json().then((data) => {
                    this.loadImages["count"] = data["count"];
                    this.loadImages["images"] = data["resp"];

                    this.loadImages.images.forEach((element: any) => {
                        element["realPath"] = `${location.toString()}/dataset/${element["path"]}`
                    });
                    this.$emit("searchResult", { searching: false, count: data["count"], time: data["time"] })
                });
            }).catch(err => {
                toast.error(err);
            }).finally(() => {
                this.loadingImages = false;
                this.$emit("searchResult", { searching: false })
            });
        },
        openFileInput() {
            const fileInput = document.querySelector('#input-file') as HTMLElement;
            if (fileInput !== null) {
                fileInput.click();
            }
        },
        handleFileChange(event: any) {
            if (this.loadingTokens) {
                toast.info("Uploading image. Please wait!");
                return;
            }
            const file = event.target.files[0];
            if (file) {
                this.uploadImage(file);
                this.$emit('fileChanged', file);
            } else {
                toast.warn("No file selected. Please try again");
            }
        },
        uploadImage(file: any) {
            this.loadingTokens = true;
            let url = `${location.toString()}api/image/token`;
            fetch(url, { method: "POST", body: file }).then((response) => {
                return response.json();
            }).then((data) => {
                if (data["error"]) {
                    toast.error(data["error"], { autoClose: 2000 });
                    this.$emit("searchResult", { searching: false, count: 0, time: 0 })
                    return;
                }
                this.loadedTokens = data["resp"];
                this.searchString = this.loadedTokens;
                this.doSearchString();
            }).catch(err => {
                toast.error(err);
            }).finally(() => {
                this.loadingTokens = false;
            });
        },
        deleteImage(imgId: number) {
            toast.info(`Deleting image`)
            let url = `${location.toString()}api/image/${imgId}`;
            fetch(url, { method: "DELETE" }).then((response) => {
                return response.json();
            }).then((data) => {
                if (data["error"]) {
                    toast.error(data["error"], { autoClose: 2000 });
                    return;
                }
                toast.success(`Deleted image`)
                this.doSearchString();
            }).catch(err => {
                toast.error(err);
            });
        },
        updateDisplaySize(size: any) {
            this.displaySizes.choose = size;
            this.displaySizes.label = `Display size [${size}]`;
            this.doSearchString();
        },
    },
    created() {
    }
}
</script>
