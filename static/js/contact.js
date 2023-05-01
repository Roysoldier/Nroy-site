function submit_contact() {
    contactName = document.getElementById('name').value
    contactSurname = document.getElementById('surname').value
    contactEmail = document.getElementById('email').value
    contactText = document.getElementById('txt').value

    if(contactName == "") {
        document.getElementById('errormessage').innerHTML = "| Prénom invalide |"
    }
    else {
        document.getElementById('errormessage').innerHTML = ""
    }
    if(contactSurname == "") {
        document.getElementById('errormessage1').innerHTML = "| Nom invalide |"
    } 
    else {
        document.getElementById('errormessage1').innerHTML = ""
    }
    if (!contactEmail.match(/^\w.+@[a-zA-Z_-]+?\.[a-zA-Z]{2,3}$/)) {
        document.getElementById('errormessage2').innerHTML = "| Email invalide |"
        }
    else {
        document.getElementById('errormessage2').innerHTML = ""
    }

    if(contactText == "") {
        document.getElementById('errormessage3').innerHTML = "| Merci de rentrer un message |"
    } 
    else {
        document.getElementById('errormessage3').innerHTML = ""
    }


    if(contactName != "" && contactSurname !="" && contactEmail.match(/^\w.+@[a-zA-Z_-]+?\.[a-zA-Z]{2,3}$/) && contactText !=  "") {
        var sendrequest = {
            "name": contactName,
            "surname": contactSurname,
            "email": contactEmail,
            "message": contactText
        }
        $(function () {
            $.ajax({
                type: 'POST',
                url: "api/contact",
                data: JSON.stringify(sendrequest),
                contentType: "application/json",
                dataType: "json", 
                success: function (result) {
                    // on va verifier le status renvoyer par flask
                    if (result.status == "ok") {
                        alertify.alert("Contact","Ton message à bien été envoyer !");
                    }
                    else {
                        // sinon on va renvoyer une pop-up d'erreur 
                        alertify.alert("contact","Une erreur s'est produite !");
    
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
}
