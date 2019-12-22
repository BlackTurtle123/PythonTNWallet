$(document).ready(function () {
    $("#send_data_transfer").click(function () {
            const value = $("#data_value").val();
            const key = $("#data_key").val();
            const fee = $("#data_fee").val();
            const type = $("#data_type").val();
            const data = {value: value, key: key, type: type, fee: parseFloat(fee)};
            console.log(data)

        }
    );
});
