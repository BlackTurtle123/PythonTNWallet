$(document).ready(function () {

    $("#tx_load").click(function () {
            const addr = $(this).data("addr");
            $("#tx_collapse_div").toggle();
            load_tx(addr, 200);

        }
    );
    $("#lease_load").click(function () {
            const addr = $(this).data("addr");
            $("#lease_collapse_div").toggle();
            load_lease(addr);

        }
    );
    $("#data_load").click(function () {
            const addr = $(this).data("addr");
            $("#data_collapse_div").toggle();
            load_data(addr);

        }
    );

    function load_tx(addr, amount) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: '/state/transactions/' + addr + '/' + amount,

        }).done(function (data) {
            let tablecontents = "";
            tablecontents = '<table>';
            tablecontents += '<tr><th>Type</th><th>Id</th><th>Sender</th><th>Amount</th><th>Asset Id</th><th>Recipient</th><th>Height</th></tr>';
            $.each(data[0], function (index, value) {

                tablecontents += "<tr class='tr'>";
                tablecontents += "<td>" + value["type"] + "</td>";
                tablecontents += "<td><a href='https://explorer.turtlenetwork.eu/tx/" + value["id"] + "'>" + value["id"] + "</a></td>";
                tablecontents += "<td>" + value["sender"] + "</td>";
                tablecontents += "<td>" + value["amount"] + "</td>";
                tablecontents += "<td>" + value["assetId"] + "</td>";
                tablecontents += "<td>" + value["recipient"] + "</td>";
                tablecontents += "<td>" + value["height"] + "</td>";
                tablecontents += "</tr>";
            });
            tablecontents += '</table>';

            $("#tx_collapse_div").html(tablecontents);

        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }

    function load_lease(addr) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: '/state/leases/' + addr,

        }).done(function (data) {
            let tablecontents = "";
            tablecontents = '<table>';
            tablecontents += '<tr><th>Type</th><th>Id</th><th>Sender</th><th>Amount</th><th>Recipient</th><th>Height</th><th>Cancel</th></tr>';
            $.each(data, function (index, value) {

                tablecontents += "<tr class='tr'>";
                tablecontents += "<td>" + value["type"] + "</td>";
                tablecontents += "<td><a href='https://explorer.turtlenetwork.eu/tx/" + value["id"] + "'>" + value["id"] + "</a></td>";
                tablecontents += "<td>" + value["sender"] + "</td>";
                tablecontents += "<td>" + value["amount"] + "</td>";
                tablecontents += "<td>" + value["recipient"] + "</td>";
                tablecontents += "<td>" + value["height"] + "</td>";
                tablecontents += "<td> <button class='cancel_lease' data-id='"+value["id"]+"'>Cancel Lease</button></td>";
                tablecontents += "</tr>";
            });
            tablecontents += '</table>';

            $("#lease_collapse_div").html(tablecontents);

        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }

    function load_data(addr) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: '/address/data/' + addr,

        }).done(function (data) {
            let tablecontents = "";
            tablecontents = '<table>';
            tablecontents += '<tr><th>Key</th><th>Type</th><th>Value</th><th>Edit value</th></tr>';
            $.each(data, function (index, value) {

                tablecontents += "<tr class='tr'>";
                tablecontents += "<td>" + value["key"] + "</td>";
                tablecontents += "<td>" + value["type"] + "</td>";
                tablecontents += "<td>" + value["value"] + "</td>";

                tablecontents += "<td> <button >----</button></td>";
                tablecontents += "</tr>";
            });
            tablecontents += '</table>';

            $("#data_collapse_div").html(tablecontents);

        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }
})
;
