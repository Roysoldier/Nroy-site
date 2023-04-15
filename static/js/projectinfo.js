
 function clickedinfo(project) {
    project = project.name
    nameproj= document.getElementById('recup_' + project).innerHTML
   

    var sendrequest = {
      "name": nameproj
  }

  $(function () {

      $.ajax({
          type: 'POST',
          url: "api/projectinfo",
          data: JSON.stringify(sendrequest),
          contentType: "application/json",
          dataType: "json",
          success: function (result) {

              if (result.status == "ok") {
               //window.location = "projetpres.html"
              }
              else {


                  //alert(result.msg);

              }
          },
          error: function (xhr, ajaxOptions, thrownError) {
              alert("Une erreur réseau est survenue");
          }
      });
  });
}
