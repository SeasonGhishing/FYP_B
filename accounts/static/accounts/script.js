// script.js

function previewImage(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
  
    reader.onload = function() {
      const image = document.createElement('img');
      image.src = reader.result;
      image.style.width = '97px';
      image.style.height = '97px';
      image.style.borderRadius = '50%'; // Set border radius to match circle
      image.style.objectFit = 'cover';
      document.querySelector('.main-content .circle').innerHTML = '';
      document.querySelector('.main-content .circle').appendChild(image);
    }
  
    reader.readAsDataURL(file);
  }
