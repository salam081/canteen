document.addEventListener('DOMContentLoaded', function() {
  var toastElement = document.getElementById('liveToast');
  var toast = new bootstrap.Toast(toastElement, {
    autohide: false
  });
  
  toast.show();
  
  setTimeout(function() {
    toast.hide();
  }, 5000);
});