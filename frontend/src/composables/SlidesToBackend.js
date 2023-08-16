import axios from "axios";

const sendSlidesToBackend = async (endpoint, slides, useGPT4) => {
    const formData = new FormData();
    formData.append('slides', slides);
    formData.append('useGPT4', useGPT4);
    const response = await axios.post("http://127.0.0.1:5000/" + endpoint, {
        slides: slides,
        useGPT4: useGPT4
    });
    return response.data;
}

export default sendSlidesToBackend;