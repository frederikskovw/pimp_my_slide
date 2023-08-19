import axios from "axios";

const sendSlidesToBackend = async (endpoint, slides, useGPT4, wordDoc=null) => {
    const formData = new FormData();
    if (wordDoc) {
        formData.append('wordDoc', wordDoc);
    } else {
        formData.append('slides', JSON.stringify(slides));
    }
    formData.append('useGPT4', useGPT4);
    const response = await axios.post("http://127.0.0.1:5000/" + endpoint, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    return response.data;
}

export default sendSlidesToBackend;
