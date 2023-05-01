function new_comment(status) {
    if (status == 0) {
      comment = document.getElementById('newcomment').value
    } else {
      comment = document.getElementById('newresponce_' + JSON.stringify(status)).value
    }
  
    proj = document.getElementById("pres-title-project").innerHTML
  
    if (comment != "" && comment != " ") {
      var sendrequest = {
        "comment": comment.replace("'", "¤"),
        "projet": proj,
        "status": status
      }
  
      $(function () {
        $.ajax({
          type: 'POST',
          url: "api/comment",
          data: JSON.stringify(sendrequest),
          contentType: "application/json",
          dataType: "json",
          success: function (result) {
            if (result.status == "ok") {
              // Enregistrez la position de défilement actuelle
              localStorage.setItem('scrollPosition', window.pageYOffset);
  
              // Rechargez la page
              location.reload();
            } else {
              alert(result.msg);
            }
          },
          error: function (xhr, ajaxOptions, thrownError) {
            alert("Une erreur réseau est survenue");
          }
        });
      });
    }
  }
  
  function delete_message(id) {
    var sendrequest = {
      "id": id
    }
  
    $(function () {
      $.ajax({
        type: 'POST',
        url: "api/deleteMessage",
        data: JSON.stringify(sendrequest),
        contentType: "application/json",
        dataType: "json",
        success: function (result) {
          if (result.status == "ok") {
            // Enregistrez la position de défilement actuelle
            localStorage.setItem('scrollPosition', window.pageYOffset);
  
            // Rechargez la page
            window.location.reload();
          } else {
            alert(result.msg);
          }
        },
        error: function (xhr, ajaxOptions, thrownError) {
          alert("Une erreur réseau est survenue");
        }
      });
    });
  }
  
  // Attendez que la page se charge complètement
  window.addEventListener('load', function () {
    // Récupérez la position de défilement enregistrée
    var scrollPosition = localStorage.getItem('scrollPosition');
  
    // Si une position de défilement a été enregistrée, faites défiler la page jusqu'à cette position
    if (scrollPosition !== null) {
      window.scrollTo(0, scrollPosition);
      // Supprimez la position de défilement enregistrée
      localStorage.removeItem('scrollPosition');
    }
  });
  