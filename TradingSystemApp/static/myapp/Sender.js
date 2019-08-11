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
                //�qpython��ݱ����쪺�ƭȶ�ihtml�e�ݼ���result���ƭ�
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
                //�qpython��ݱ����쪺�ƭȶ�ihtml�e�ݼ���result���ƭ�
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