function sign_up() {
    var pseudo = document.getElementById("pseudo").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var passwordv = document.getElementById("passwordv").value;

    if (passwordv == password) {
        var sendrequest = {
            "pseudo": pseudo,
            "email": email,
            "password": password
        }

        $(function () {

            $.ajax({
                type: 'POST',
                url: "api/signup",
                data: JSON.stringify(sendrequest),
                contentType: "application/json",
                dataType: "json",
                success: function (result) {

                    if (result.status == "ok") {
                        alert(result.msg);
                        window.location = "signin.html";
                    }
                    else {
                        alert(result.msg);
    
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    alert("Une erreur réseau est survenue");
                }
            });
        });
        
    }

    else {
        alert("password non identique")
    }

}