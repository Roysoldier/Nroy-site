function sign_in() {
    
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    
    if (email == "") {
        document.getElementById('errormessage').innerHTML = "Adresse email invalide"
    }
    else {
        document.getElementById('errormessage').innerHTML = ""
    }
    if (password == "") {
        document.getElementById('errormessage1').innerHTML = "Mot de passe invalide"
    }
    else {
        document.getElementById('errormessage1').innerHTML = ""
    }
    
    if (password != "" && email != "") {
        var sendrequest = {
            "email": email,
            "password": password
        }
        
        $(function () {
            
            $.ajax({
                type: 'POST',
                url: "api/signin",
                data: JSON.stringify(sendrequest),
                contentType: "application/json",
                dataType: "json",
                success: function (result) {
    
                    if (result.status == "ok") {
                        //alert(result.msg);
                        //var cookie = window.Cookies.get();
                        //alert(JSON.stringify(cookie))
                        
                        window.location = "index.html";
                    }
                    else {
                        if(result.msg == "mdp incorrect"){
                            document.getElementById('errormessage1').innerHTML = "Mot de passe invalide"
                        }
                        else {
                            document.getElementById('errormessage1').innerHTML = ""
                        }
                        if(result.msg == "error") {
                            document.getElementById('errormessageb').innerHTML = "Adresse mail ou mot de passe invalide"
                        }
                        else{
                            document.getElementById('errormessageb').innerHTML = ""
                        }

                        //alert(result.msg);
    
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    alert("Une erreur réseau est survenue");
                }
            });
        });
    }
    
}