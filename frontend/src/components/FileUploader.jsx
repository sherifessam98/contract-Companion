import React, {useState} from "react";
import {uploadFile} from "../services/api";


export default function FileUploader({onUploaded}){
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState("");
//     Handling File input change
    const handleChange = (e) => {
        setFile(e.target.files[0]); // grabs the first file selected
        setStatus(""); // clears any old status
        };
    //  Upload when form is submitted
    const handleSubmit = async (e) => {
        e.preventDefault(); // stops the page from refreshing
        if(!file){
            setStatus("Please select a file first.");
            return;
            }

        setStatus("Uploading..");
        try {
          const res = await uploadFile(file);
          setStatus(`Indexed: ${res.data.filename}`);
          onUploaded(); // Notifying parent that uplaod is done
        } catch(err){
            setStatus("Upload failed.");
            console.error(err)
            }
    };

    return(
        <div>
            <form onSubmit = {handleSubmit}>
                <input type="file" accept=".pdf,.docx,.txt" onChange={handleChange} />
                <button type="submit">Upload Document</button>
            </form>
            <p>{status}</p>
        </div>
        );
    }