function sign_in() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

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
                    alert(result.msg);
                    window.location = "index.html";
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