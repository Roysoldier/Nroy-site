
function modif_bio() {
    if (document.getElementById('modif-bio').hidden) {

        document.getElementById('modif-bio').hidden = false
        document.getElementById('area-bio').innerHTML = " "
        document.getElementById('bio').hidden = true
    }
    else {
        document.getElementById('area-bio').innerHTML = ''
        document.getElementById('modif-bio').hidden = true
        document.getElementById('bio').hidden = false
    }

}

function modif_bio_valid() {

    bio = document.getElementById('area-bio').value
    if (bio.length > 0 && bio.length < 125) {
        document.getElementById('modif-bio').hidden = true
        var sendrequest = {
            "bio": bio.replace("'", '"')
        }

        $(function () {

            $.ajax({
                type: 'POST',
                url: "api/bio",
                data: JSON.stringify(sendrequest),
                contentType: "application/json",
                dataType: "json",
                success: function (result) {

                    if (result.status == "ok") {
                        window.location.reload()
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
}




