async function openDirectoryPicker() {
  try {
    const directoryHandle = await window.showDirectoryPicker();
    console.log('Directory selected:', directoryHandle.name);
    // You can then use the directoryHandle to access files within the selected directory.
  } catch (error) {
    console.error('Error opening directory picker:', error);
  }
}

document.addEventListener('click', e => {
    const lmt = e.target;
    if (lmt.classList.contains('select-bt')) openDirectoryPicker();
});
