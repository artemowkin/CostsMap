<script setup>
import DeleteIcon from '../assets/icons/delete.svg'

const props = defineProps(['showForm', 'deleteAction'])
</script>

<template>
    <div class="popup_form_container">
        <div class="close_div" @click="props.showForm(false)"></div>
        <form class="actions_list">
            <div class="action delete_action" @click="props.deleteAction()">
                <div class="delete_action_icon">
                    <img :src="DeleteIcon" />
                </div>
                <div class="action_title">delete</div>
            </div>
        </form>
    </div>
</template>

<style>
.actions_list {
    flex-direction: row;
}

.action {
    cursor: pointer;
}

.delete_action {
    display: grid;
    place-items: center;
    gap: .5em;
}

.delete_action_icon {
    width: 50px;
    height: 50px;
    background: rgba(255, 0, 0, .2);
    border-radius: 10px;
    display: grid;
    place-content: center;
}

.delete_action_icon img {
    width: 30px;
    height: 30px;
    background-size: cover;
}
</style>