import React, { useState } from "react";
import axios from "axios";

export default function FaceUploadForm() {
  const [name, setName] = useState("");
  const [folderPath, setFolderPath] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [downloading, setDownloading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !folderPath || !imageFile) return alert("Fill all fields");

    const formData = new FormData();
    formData.append("user_name", name);
    formData.append("folder_path", folderPath);
    formData.append("input_image", imageFile);

    setDownloading(true);
    try {
      const response = await axios.post("http://localhost:5000/match-faces", formData, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = `${name}_matches.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Failed to process: " + error.message);
    }
    setDownloading(false);
  };


  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto bg-white p-6 shadow-md rounded">
      <label className="block mb-2 font-medium">Your Name</label>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)}
        className="w-full border mb-4 p-2 rounded" />
      <label className="block mb-2 font-medium">Folder Path</label>
      <input type="text" value={folderPath} onChange={(e) => setFolderPath(e.target.value)}
        className="w-full border mb-4 p-2 rounded" />
      <label className="block mb-2 font-medium">Image File</label>
      <input type="file" accept="image/*" onChange={(e) => setImageFile(e.target.files[0])}
        className="w-full border mb-4 p-2 rounded" />
      <button type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        disabled={downloading}>
        {downloading ? "Processing..." : "Submit"}
      </button>
    </form>
  );
}
