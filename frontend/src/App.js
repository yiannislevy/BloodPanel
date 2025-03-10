import React, { useState } from 'react';
import Upload from "./Upload";

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileUpload = (file) => {
    console.log("File selected:", file);
    setSelectedFile(file);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px"}}>
      <h1>Upload Blood Test</h1>
      <Upload onFileUpload={handleFileUpload} />
      {selectedFile && <p>Selected File: {selectedFile.name}</p>}
    </div>
  );
};

export default App;
