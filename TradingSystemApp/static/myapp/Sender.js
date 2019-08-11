$(document).ready(function () {
    $("#btnUpdateOneStock").click(function () {
        var market = $("#market").val();
        var stockId = $("#stockId").val();        
        $.ajax({
            type: 'GET',
            url: "/UpdatingStockDb",
            data: {
                'market': market,
                'stockId': stockId                
            },
            success: function (Data) {
                //從python後端接收到的數值塞進html前端標籤result的數值
                $("#result").html(Data)
            },
            error: function (e) {

                console.log(e);
            }
        })

    });
});

$(document).ready(function () {
    $("#btnSetTurtleParam").click(function () {
        var stockIdForTurtle = $("#stockIdForTurtle").val();
        var calculatingDays = $("#calculatingDays").val();
        $.ajax({
            type: 'GET',
            url: "/TurtleResult",
            data: {
                'stockIdForTurtle': stockIdForTurtle,
                'calculatingDays': calculatingDays
            },
            success: function (Data) {
                //從python後端接收到的數值塞進html前端標籤result的數值
                data = JSON.parse(Data);
                $("#StockQtyForEveryUnit").html(data["a"]);
                $("#OverWeightList").html(data["b"]);
                $("#StopPriceList").html(data["c"]);
            },
            error: function (e) {

                console.log(e);
            }
        });

    });
});