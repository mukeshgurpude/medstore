ids = ["id_name", "id_category", "id_description", "id_quantity", "id_price"]
for(id in ids){
    $("#"+ids[id]).addClass("form-control");
}

$("#id_thumbnail").addClass("form-control-file")
$("input[value=Submit").addClass("btn btn-default")
$("input[value=Cancel").addClass("btn btn-danger")


