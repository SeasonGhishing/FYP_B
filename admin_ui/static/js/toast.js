function showToast(message, type) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.classList.add('toast');
    if (type === 'success') {
      toast.classList.add('success');
    } else if (type === 'error') {
      toast.classList.add('error');
    }
    document.body.appendChild(toast);
  
    setTimeout(() => {
      toast.classList.add('show');
    }, 100);
  
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        toast.remove();
      }, 500); // Transition duration + delay before removing
    }, 3000); // Adjust duration as needed
  }