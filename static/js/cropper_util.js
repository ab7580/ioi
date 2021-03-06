window.addEventListener('DOMContentLoaded', function () {
    var initialAvatarURL;
    var avatar = document.getElementById('imageResult');
    initialAvatarURL = avatar.src;
    var image = document.getElementById('image');
    var input = document.getElementById('upload');
    var myText = document.getElementById("myText");
    var slikaName = document.getElementById("slika_name");
    var $progress = $('.progress');
    var $progressBar = $('.progress-bar');
    var $alert = $('.alert');
    console.log($alert);
    var $modal = $('#modal');
    var cropper;

    $('[data-toggle="tooltip"]').tooltip();

    input.addEventListener('change', function (e) {
      var files = e.target.files;
      var done = function (url) {
        input.value = '';
        image.src = url;
        $alert.hide();
        $modal.modal('show');
      };
      var reader;
      var file;
      var url;

      if (files && files.length > 0) {
        file = files[0];

        if (URL) {
          done(URL.createObjectURL(file));
        } else if (FileReader) {
          reader = new FileReader();
          reader.onload = function (e) {
            done(reader.result);
          };
          reader.readAsDataURL(file);
        }
      }
    });

    $modal.on('shown.bs.modal', function () {
      cropper = new Cropper(image, {
        aspectRatio: 1,
        viewMode: 3,
        minCropBoxWidth: 100,
        minCropBoxHeight: 100,
      });
    }).on('hidden.bs.modal', function () {
      cropper.destroy();
      console.log("destroying modal");
      cropper = null;
    });

    document.getElementById('close').addEventListener('click', function () {
      avatar.src = initialAvatarURL;
    });

    document.getElementById('crop').addEventListener('click', function () {
      var canvas;

      $modal.modal('hide');

      if (cropper) {
        canvas = cropper.getCroppedCanvas({
          width: 400,
          height: 400,
          
        });
        avatar.src = canvas.toDataURL();
        $progress.show();
        $alert.removeClass('alert-success alert-warning');
        canvas.toBlob(function (blob) {
            var formData = new FormData();
            var uuid = crypto.randomUUID();
            slikaName.value = uuid + '.jpg';
            formData.append('slika', blob, slikaName.value);
          $.ajax('http://127.0.0.1:8000/upload', {
            method: 'POST',
            data: formData,
            processData: false,
              contentType: false,
              headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },

            xhr: function () {
              var xhr = new XMLHttpRequest();

              xhr.upload.onprogress = function (e) {
                var percent = '0';
                var percentage = '0%';

                if (e.lengthComputable) {
                  percent = Math.round((e.loaded / e.total) * 100);
                  percentage = percent + '%';
                  $progressBar.width(percentage).attr('aria-valuenow', percent).text(percentage);
                }
              };

              return xhr;
            },

            success: function () {
              initialAvatarURL = avatar.src;
              $alert.show().addClass('alert-success text-center').text('Nalaganje uspe??no');
            },

            error: function () {
              avatar.src = initialAvatarURL;
              $alert.show().addClass('alert-warning text-center').text('Napaka pri nalaganju na stre??nik');
            },

            complete: function () {
              if (myText) {
                myText.remove();
              }
              $progress.hide();
            },
          });
        });
      }
    });
  });