<template>
    <nav>
        <span @click="router.push({ name: 'Home' })" class="material-symbols-outlined">home</span>
    </nav>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
    setup () {
        const router = useRouter();
        return { router }
    }
}
</script>

<style>
nav {
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 10vh;
    box-shadow: 0 0 10px 0 rgb(28, 49, 49);
    margin-bottom: 30px;
}
</style>