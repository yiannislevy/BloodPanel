import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

const Upload = ({ onFileUpload }) => {
    const [errorMessage, setErrorMessage] = useState("");
    const [isUploading, setIsUploading] = useState(false);
    
    // define handleFileUpload with useCallback to avoid ESLint warnings
    const handleFileUpload = useCallback(async (file) => {
        const formData = new FormData();
        formData.append("file", file);
        
        setIsUploading(true);
        
        try {
            // Send file to FastAPI
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData,
            });
            
            // Parse response data
            const data = await response.json();
            
            if (!response.ok) {
                // Server returned an error
                setErrorMessage(data.error || "Upload failed. Please try again.");
                console.error("Upload failed:", data);
            } else {
                // success
                console.log("Upload successful:", data);
                alert(`Upload successful! File: ${file.name}`);
                // Call parent callback if provided
                if (onFileUpload) {
                    // Pass both the original file and the server response
                    onFileUpload({
                        ...data,
                        name: file.name,
                        originalFile: file
                    });
                }
            }
        } catch (error) {
            setErrorMessage("Error connecting to server. Please try again.");
            console.error("Error uploading file:", error);
        } finally {
            setIsUploading(false);
        }
    }, [onFileUpload, setErrorMessage, setIsUploading]);
    
    const onDrop = useCallback(async (acceptedFiles, fileRejections) => {
        // Clear previous error messages
        setErrorMessage("");
        
        // Handle file rejections from react-dropzone (non-PDF files)
        if (fileRejections && fileRejections.length > 0) {
            setErrorMessage("Please upload a valid PDF file.");
            return;
        }
        
        // If we have accepted files, upload the first one
        if (acceptedFiles && acceptedFiles.length > 0) {
            await handleFileUpload(acceptedFiles[0]);
        }
    }, [handleFileUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"]
        },
        maxFiles: 1
    });

    // Removed this function as it's now defined with useCallback above

    return (
        <div className="upload-container">
            <div 
                {...getRootProps()}
                style={{
                    border: errorMessage ? "2px dashed #dc3545" : isDragActive ? "2px dashed #28a745" : "2px dashed #007bff",
                    padding: "20px",
                    textAlign: "center",
                    cursor: "pointer",
                    borderRadius: "10px",
                    width: "300px",
                    margin: "20px auto",
                    backgroundColor: isDragActive ? "#f8f9fa" : "transparent",
                    transition: "all 0.2s ease"
                }}
            >
                <input {...getInputProps()} />
                {isUploading ? (
                    <p>Uploading...</p>
                ) : (
                    <p>{isDragActive ? "Drop the PDF here" : "Drag & Drop a PDF here, or click to browse"}</p>
                )}
            </div>
            
            {errorMessage && (
                <div style={{
                    color: "#dc3545",
                    textAlign: "center",
                    marginTop: "10px",
                    padding: "8px",
                    borderRadius: "5px",
                    backgroundColor: "#f8d7da",
                    width: "300px",
                    margin: "0 auto"
                }}>
                    {errorMessage}
                </div>
            )}
        </div>
    );
};

export default Upload;