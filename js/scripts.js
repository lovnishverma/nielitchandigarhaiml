// Show the "Go to Top" button when the user scrolls down
window.addEventListener('scroll', function() {
  const scrollToTopButton = document.querySelector('.go-to-top');
  if (window.pageYOffset > 300) {
    scrollToTopButton.classList.add('show');
  } else {
    scrollToTopButton.classList.remove('show');
  }
});