import React, { useState } from 'react';
import Upload from "./Upload";

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileUpload = (fileData) => {
    console.log("File uploaded:", fileData);
    setSelectedFile(fileData);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px"}}>
      <h1>Upload Blood Test</h1>
      <Upload onFileUpload={handleFileUpload} />
      {selectedFile && (
        <div>
          <p>Selected File: {selectedFile.originalFile?.name || selectedFile.filename || selectedFile.name}</p>
        </div>
      )}
    </div>
  );
};

export default App;