// Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        document.getElementById("upload").required = false;
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            console.log("halt!");
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();

  function validate_pw2(pw2) {
    if (pw2.value !== $("#password").val()) {
      pw2.setCustomValidity("Gesli se ne ujemata!");
    } else {
      pw2.setCustomValidity(""); // is valid
    }
  };