<template>
  <div class="page-wrapper body-content">
    <h1>Pimp my slides</h1>
    
    <div v-if="!updatedSlides" class="vertical-flex">
    <p class="centered-text">Add your content below.</p>
      <div v-for="(slide, index) in slides" :key="index" class="card">
        <div class="horizontal-flex-right">
          <p>Slide {{ index + 1 }} |</p>
          <span @click="addSlide" class="material-symbols-outlined inverse-symbol">add</span>
          <span @click="deleteSlide(index)" class="material-symbols-outlined inverse-symbol">delete</span>
        </div>
              
        <label>Lead-in</label>
        <textarea v-model="slide.leadIn" placeholder="'Chamberlain Coffee increases revenue in May'" rows="1"></textarea>

        <label>Content</label>
        <textarea v-model="slide.content" placeholder="'• Chamberlain Coffee landed Revenue ended at DKK 900.9M in May, coming in above target of DKK 800M.'
'• However, above budgeted EBITDA driven by salary cost being lower than expected.'
'• Chamberlain RTD (Ready-to-drink) was a successful launch where we delivered on-time delivery.'"
        rows="3"></textarea>

        <label>Data</label>
        <textarea v-model="slide.data" placeholder="'Bar graph showing revenue growth during 2005-2013'" rows="1"></textarea>
      </div>

      <label for="wordUpload" class="white">Or upload Word document.</label>
      <input type="file" class="tag" accept=".doc,.docx" @change="handleWordUpload" ref="fileInput" />
    </div>


    <div class="card" v-if="updatedSlides">
      <h2>Updated slide suggestions</h2>
      <p v-html="updatedSlides"></p>
    </div>

    <div class="card" v-if="flowReview">
      <h2>Review of flow</h2>
      <p v-html="flowReview.horizontalFlowReview"></p>
      <p v-html="flowReview.verticalFlowReview"></p>
    </div>

    <div class="card" v-if="execSum">
      <h2>Executive summary</h2>
      <p v-html="execSum"></p>
    </div>

    <div class="vertical-flex">
      <div class="horizontal-flex">
        <button @click="fixSlides" v-if="!updatedSlides">Pimp my slides</button>
        <button @click="fixSlides" v-if="updatedSlides">Redo my slides</button>
        <button @click="reviewFlow" v-if="updatedSlides">Review flow</button>
        <button @click="writeExecSum" v-if="updatedSlides">Write execsum</button>
      </div>
      <div class="horizontal-flex">
        <input type="checkbox" v-model="useGPT4">
        <p class="light-text notice"><b>Use GPT-4 instead of GPT-3.5 </b>(improved results, but slower). If you encounter errors with GPT-4, try using GPT-3.5.</p>
      </div>
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
    const flowReview = ref(null);
    const router = useRouter();
    const useGPT4 = ref(true);
    const loading = ref(false);
    const slides = ref([{
      leadIn: '',
      content: '',
      data: ''
    }]);
    const wordDoc = ref(null);
    const updatedSlides = ref(null);
    const execSum = ref(null);

    const addSlide = () => {
      slides.value.push({ leadIn: '', content: '', data: '' });
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
      if (wordDoc.value) {
          updatedSlides.value = await sendSlidesToBackend('fix-slides', null, useGPT4.value, wordDoc.value);
      } else {
          updatedSlides.value = await sendSlidesToBackend('fix-slides', slides.value, useGPT4.value);
      }
      loading.value = false;
    }

    const handleWordUpload = async (event) => {
      wordDoc.value = event.target.files[0];
    }

    const reviewFlow = async () => {
      loading.value = true;
      flowReview.value = await sendSlidesToBackend('review-flow', updatedSlides.value, useGPT4.value);
      loading.value = false;
    }

    const writeExecSum = async () => {
      loading.value = true;
      execSum.value = await sendSlidesToBackend('write-execsum', updatedSlides.value, useGPT4.value);
      loading.value = false;
    }

    return { router, useGPT4, fixSlides, loading, slides, addSlide, deleteSlide, updatedSlides, reviewFlow, flowReview, writeExecSum, execSum, handleWordUpload, wordDoc  }
  }
}
</script>

<style scoped>
h1 {
  margin-bottom: 50px;
}

h2, h3 {
  color: #021634;
}

h2 {
  margin-bottom: 20px;
}

h3 {
  margin-top: 20px;
}

.horizontal-flex {
  padding: 20px;
  column-gap: 10px;
}

</style>
