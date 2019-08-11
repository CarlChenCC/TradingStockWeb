
    function sender(){
        var stockId = $("#stockId").val();
        var calulatingDays = $("#calculatingDays").val();
        $.ajax({
            type: 'GET',
            url: "/result",
            data: {
                'stockId': stockId,
                'calculatingDays': calculatingDays
            },
            success: function (Data) {

                $("#result").html(Data)
            },
            error: function (e) {

                console.log(e);
            }
        })

    }

