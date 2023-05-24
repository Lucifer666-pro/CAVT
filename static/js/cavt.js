

const form = document.querySelector('form');
const loadingContainer = document.getElementById('loading-container');
const progressBar = document.getElementById('progress-bar');
const videoContainer = document.getElementById('video-container');
const videoElement = document.getElementById('translated-video');
const errorMessage = document.getElementById('error-message');

form.addEventListener('submit', function(event) {
  event.preventDefault();

  const initialLanguage = document.getElementById('initial_language').value;
  const finalLanguage = document.getElementById('final_language').value;

  const youtubeLink = document.getElementById('youtube_link').value.trim();
  const file = document.getElementById('file').files[0];
    
        if (!file && !youtubeLink) {
          errorMessage.textContent = 'Please upload a file or enter a YouTube link.';
          errorMessage.style.display = 'block';
          return;
        }
    
        if (file && youtubeLink) {
          errorMessage.textContent = 'Please choose either a file or a YouTube link, not both.';
          errorMessage.style.display = 'block';
          return;
        }

  if (initialLanguage === finalLanguage) {
    errorMessage.textContent = 'Please select different languages.';
    errorMessage.style.display = 'block';
    return;
  }

  errorMessage.style.display = 'none';
  loadingContainer.setAttribute('aria-busy', 'true');
  progressBar.style.display = 'block';
  progressBar.ariaLabel='Content loading…'
  //progressBar.value = 0;

  const formData = new FormData(form);

  fetch('/translate', {
    method: 'POST',
    body: formData,
    onUploadProgress: function(progressEvent) {
      const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
      progressBar.value = progress;
    }
  })
    .then(response => response.blob())
    .then(blob => {
      const videoUrl = URL.createObjectURL(blob);
      videoElement.src = videoUrl;
      videoContainer.style.display = 'block';
      progressBar.style.display = 'none';
      loadingContainer.setAttribute('aria-busy', 'false');
    })
    .catch(error => {
      console.error('Translation error:', error);
    });
});




