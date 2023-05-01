function sign_out() {
    var sendrequest = {
        "message": "Compte déconnecter"
    }
    $(function () {
        $.ajax({
            type: 'POST',
            url: "api/signout",
            data: JSON.stringify(sendrequest),
            contentType: "application/json",
            dataType: "json", 
            success: function (result) {
                // on va verifier le status renvoyer par flask
                if (result.status == "ok") {
                    // alert("réussite")
                    window.location = "index.html";
                }
                else {
                    // sinon on va renvoyer une pop-up d'erreur 
                    ;

                }
            },
            // si il y a une erreur 
            error: function (xhr, ajaxOptions, thrownError) {
                // on renvoie une pop-up d'erreur 
                alert("erreur")
            }
        });
    });
}
