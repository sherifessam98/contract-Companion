import axios from "axios";


//Creating an Axios instance with the base URL of the backend
const api = axios.create({
    baseURL: "http://localhost:8000",});

//Uploading file to /upload endpoint
export function uploadFile(file){
    const formData = new FormData();
    formData.append("file",file);
    return api.post("/upload",formData,{
    headers: {"Content-Type":"multipart/form-data"},// tell backend we're sending a file
    });
}

// Sending a question to /query endpoint
export function askQuestion(question){
    return api.post("/query",{question});
}

export default api