import axios from "axios";

const sendSlidesToBackend = async (endpoint, slides, useGPT4, wordDoc = null) => {
  const formData = new FormData();
  if (wordDoc) {
    formData.append('wordDoc', wordDoc);
  } else {
    formData.append('slides', JSON.stringify(slides));
  }
  formData.append('useGPT4', useGPT4);
  
  const initialResponse = await axios.post("/api/" + endpoint, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  const taskId = initialResponse.data.task_id;

  return new Promise((resolve, reject) => {
    const pollTaskStatus = async () => {
      try {
        const statusResponse = await axios.get(`/api/task-status/${taskId}`);
        const taskState = statusResponse.data.state;

        if (taskState !== "PENDING") {
          resolve(statusResponse.data.status);
        } else {
          // Poll again after 5 seconds
          setTimeout(pollTaskStatus, 5000);
        }
      } catch (error) {
        reject(error);
      }
    };
    
    pollTaskStatus();
  });
}

export default sendSlidesToBackend;
