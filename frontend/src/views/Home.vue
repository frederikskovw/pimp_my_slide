<template>
  <div class="page-wrapper body-content">
    <h1>Fix my slides</h1>
    <p class="centered-text">Add your content below.</p>

    <div v-for="(slide, index) in slides" :key="index" class="card">
      <div class="horizontal-flex-right">
        <p>Slide {{ index + 1 }} |</p>
        <span @click="addSlide" class="material-symbols-outlined inverse-symbol">add</span>
        <span @click="deleteSlide(index)" class="material-symbols-outlined inverse-symbol">delete</span>
      </div>
            
      <label>Lead-in</label>
      <textarea v-model="slide.leadIn" placeholder="Chamberlain Coffee increases revenue in May" rows="1"></textarea>

      <label>Content</label>
      <textarea v-model="slide.content" placeholder="• Chamberlain Coffee landed Revenue ended at DKK 900.9M in May, coming in above target of DKK 800M.
• However, above budgeted EBITDA driven by salary cost being lower than expected.
• Chamberlain RTD (Ready-to-drink) was a successful launch where we delivered on-time delivery."
      rows="3"></textarea>
    </div>


    <div class="vertical-flex">
      <div class="horizontal-flex">
        <button @click="fixSlides">Fix my slides</button>
      </div>
      <div class="horizontal-flex">
        <input type="checkbox" v-model="useGPT4">
        <p class="light-text notice"><b>Check this box to use GPT-4 instead of GPT-3.5 </b>(improved results, but slower). If you encounter errors with GPT-4, try using GPT-3.5.</p>
      </div>
    </div>

    <div>
      <p v-html="updatedSlides"></p>
    </div>
    
    <div class="vertical-flex">
      <div v-if="loading" class="spinner"></div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import sendSlidesToBackend from '../composables/SlidesToBackend.js';

export default {
  setup () {
    const router = useRouter();
    const useGPT4 = ref(false);
    const loading = ref(false);
    const slides = ref([{
      leadIn: '',
      content: ''
    }]);
    const updatedSlides = ref(null);

    const addSlide = () => {
      slides.value.push({ leadIn: '', content: '' });
    };

    const deleteSlide = (index) => {
      if (slides.value.length > 1) {
        slides.value.splice(index, 1);
        return;
      }
      console.log('Cannot delete last slide');
      return;
    };

    const fixSlides = async () => {
      loading.value = true;
      updatedSlides.value = await sendSlidesToBackend('fix-slides', slides.value, useGPT4.value);
      loading.value = false;
    }

    return { router, useGPT4, fixSlides, loading, slides, addSlide, deleteSlide, updatedSlides }
  }
}
</script>

<style scoped>
h1 {
  margin-bottom: 30px;
}

.horizontal-flex {
  padding: 20px;
  column-gap: 10px;
}

.centered-text {
  margin-bottom: 50px;
}

</style>
