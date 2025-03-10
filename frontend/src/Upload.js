import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

const Upload = ({ onFileUpload }) => {
    const onDrop = useCallback(acceptedFiles => {
        if (acceptedFiles.length > 0) {
            // Ensure the file is a PDF
            const file = acceptedFiles[0];
            if (file.type === "application/pdf") {
                onFileUpload(file); // Process only PDFs
            } else {
                console.error("Please upload a valid PDF file.");
            }
        }
    }, [onFileUpload]);

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"]
        } // Ensure only PDFs are accepted
    });

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
