function sign_up() {
    var pseudo = document.getElementById("pseudo").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var passwordv = document.getElementById("passwordv").value;
    if (pseudo.lengt > 12){
        document.getElementById('errormessage').innerHTML = 'Maximum 12 caractère'
        
    }
    else{
        document.getElementById('errormessage').innerHTML = ''
    }
    if (pseudo.length < 4){
        document.getElementById('errormessage').innerHTML = 'Minimum 4 caractères'
    }
    else if (pseudo.length <= 12){
        document.getElementById('errormessage').innerHTML = ''
    }
    if (!email.match(/^\w.+@[a-zA-Z_-]+?\.[a-zA-Z]{2,3}$/)){
        document.getElementById('errormessage1').innerHTML = "L'email est invalide"
    }
    else{
        document.getElementById('errormessage1').innerHTML = ''
    }
    if (password.length < 6){
        document.getElementById('errormessage2').innerHTML = 'Minimum 6 caractères'
    }
    else{
        document.getElementById('errormessage2').innerHTML = ''
    }
    if (passwordv != password){
        document.getElementById('errormessage3').innerHTML = 'Les mots de passe ne correspondent pas !'
    }
    else{
        document.getElementById('errormessage3').innerHTML = ''
    }
        
    if (passwordv == password && pseudo.length <= 12 && pseudo.length >= 4 && email.match(/^\w.+@[a-zA-Z_-]+?\.[a-zA-Z]{2,3}$/) && password.length > 6) {
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
                        if (result.msg == 'email already exists'){
                            document.getElementById('errormessage1').innerHTML = 'Email déja existant !'
                        }
                        else{
                            document.getElementById('errormessage1').innerHTML = ''
                        }
                        if (result.msg == 'user already exists'){
                            document.getElementById('errormessage').innerHTML = 'Pseudo déja existant !'
                        }
                        else{
                            document.getElementById('errormessage').innerHTML = ''
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

    else {
        //alert("password non identique")
    }

}