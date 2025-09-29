async function uploadFiles() {
  const input = document.getElementById("fileInput");
  const files = input.files;

  if (!files.length) {
    alert("Please select at least one JSON file.");
    return;
  }
  readFiles(files)
}

function readFiles(files) {
  const fs = require('fs')
  for (file of files) {
    const data = fs.readFileSync(file.name, 'utf8');
    console.log(data);
  }
}

document.addEventListener('click', e => {
  const lmt = e.target;
  if (lmt.classList.contains('gen-btn')) uploadFiles();
});
