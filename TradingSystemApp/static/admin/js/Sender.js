$(document).ready(function () {
    $("#btnSetTurtleParam").click(function () {
        var stockId = $("#stockId").val();
        var calulatingDays = $("#calulatingDays").val();
        $.ajax({
            type: 'GET',
            url: "/result",
            data: {
                'stockId': stockId,
                'calculatingDays': calculatingDays
            },
            success: function (Data) {

                $("#calulatingDays").html(Data)
            },
            error: function (e) {

                console.log(e);
            }
        })

    });
});