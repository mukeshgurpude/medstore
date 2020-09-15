$("input[value=Submit").addClass("btn btn-default")
$("input[value=Cancel").addClass("btn btn-danger")

tags = document.getElementsByClassName("form-control");
hide = document.getElementById("hide");
hide.addEventListener("click", function(){
    sub = document.getElementById("submit");
    if(sub.style.display == "none"){
        hide.innerHTML = "Cancel";
        sub.style.display = "";
        for(var tag=0; tag<4; tag++){
            tags[tag].removeAttribute("readonly");
            tags[tag].removeAttribute("disabled");
        };
    }
    else{
        hide.innerHTML = "Edit";
        sub.style.display = "none";
        for(var tag=0; tag<4; tag++){
            tags[tag].setAttribute("readonly", "");
            tags[tag].setAttribute("disabled", "");
        };
    }
    return false;
})

for(var p=0; p<tags.length;){
    tags[p].setAttribute("readonly", "");
    tags[p].setAttribute("disabled", "");
    p++;
}

