<script setup>
import { computed, ref } from 'vue'
import axios from '../axiosInstance'
import { useCategoriesStore } from '../stores/categories';

const categoriesStore = useCategoriesStore()

const props = defineProps(['setShowForm'])

const title = ref("")
const costsLimit = ref("")
const color = ref("#000000")
const isTitleValid = ref(false)
const isCostsLimitValid = ref(true)
const showError = ref(false)

const titleInput = (el) => {
    const elementValue = el.target.value

    title.value = elementValue

    if(elementValue.length > 0 && elementValue.length <= 15) {
        isTitleValid.value = true
    } else {
        isTitleValid.value = false
    }
}

const costsLimitInput = (el) => {
    const elementValue = el.target.value

    costsLimit.value = elementValue

    if (elementValue === "" || elementValue > 0 && elementValue < 100000) {
        isCostsLimitValid.value = true
    } else {
        isCostsLimitValid.value = false
    }
}

const submitClass = computed(() => {
    const isFormCompleted = isTitleValid.value && isCostsLimitValid.value
    return isFormCompleted ? 'completed_submit_button' : ''
})

const sendCreateCategory = async () => {
    if (!isTitleValid.value || !isCostsLimitValid.value) return

    const requestData = {
        title: title.value,
        color: color.value
    }

    if (costsLimit.value !== "") requestData.costsLimit = +costsLimit.value

    const token = JSON.parse( localStorage.getItem('tokenData') ).token

    try {
        await axios.post('/categories/', requestData, {
            headers: { Authorization: `Bearer ${token}` }
        })

        categoriesStore.loadCategories(true)

        props.setShowForm(false)
    } catch (err) {
        showError.value = true
    }
}
</script>

<template>
    <div class="popup_form_container">
        <div class="close_div" @click="props.setShowForm(false)"></div>
        <form @submit.prevent="sendCreateCategory">
            <h2>New category</h2>
            <div class="error_message" :style="showError ? { display: 'block' } : { display: 'none' }">Error with sending request</div>
            <input
                type="text"
                placeholder="Category Title"
                @click="showError = false"
                @input="titleInput"
                :value="title"
                :style="!isTitleValid && title ? { borderColor: '#aa0000' } : {}"
                required />
            <input
                inputmode="decimal"
                placeholder="Costs Limit"
                @click="showError = false"
                @input="costsLimitInput"
                :value="costsLimit"
                :style="!isCostsLimitValid ? { borderColor: '#aa0000' } : {}" />
            <input type="color" v-model="color" @click="showError = false" />
            <button :class="submitClass" type="submit">Add Category</button>
        </form>
    </div>
</template>