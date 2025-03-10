import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

const Upload = ({ onFileUpload }) => {
    const onDrop = useCallback(acceptedFiles => {
        if (acceptedFiles.length > 0) {
            // Ensure the file is a PDF
            const file = acceptedFiles[0];
            if (file.type === "application/pdf") {
                handleFileUpload(file); // Process only PDFs
            } else {
                console.error("Please upload a valid PDF file.");
            }
        }
    }, []);

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"]
        } // Ensure only PDFs are accepted
    });

    // Renamed function to avoid conflict with prop
    const handleFileUpload = async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        try {
            // Send file to FastAPI
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Upload successful:", data);
                // You can process the uploaded file data here (e.g., show filename or process for OCR)
            } else {
                const errorData = await response.json();
                console.error("Upload failed:", errorData);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    return (
        <div 
            {...getRootProps()}
            style={{
                border: "2px dashed #007bff",
                padding: "20px",
                textAlign: "center",
                cursor: "pointer",
                borderRadius: "10px",
                width: "300px",
                margin: "20px auto",
            }}
        >
            <input {...getInputProps()} />
            <p>Drag & Drop a PDF here, or click to browse</p>
        </div>
    );
};

export default Upload;
