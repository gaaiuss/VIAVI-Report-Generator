async function uploadFiles() {
  const input = document.getElementById("fileInput");
  const files = input.files;

  if (!files.length) {
    alert("Please select at least one JSON file.");
    return;
  }

  const formData = new FormData();
  for (let file of files) {
    formData.append("files", file); // "files" must match your backend field name
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/upload", { // your backend URL here
      method: "POST",
      body: formData
    });

    if (response.ok) {
      const result = await response.json();
      alert("Files uploaded successfully: " + JSON.stringify(result));
    } else {
      alert("Upload failed: " + response.statusText);
    }
  } catch (err) {
    console.error(err);
    alert("Error uploading files.");
  }
}

document.addEventListener('click', e => {
  const lmt = e.target;
  if (lmt.classList.contains('upl-btn')) uploadFiles();
});
