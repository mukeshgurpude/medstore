const submit_button = document.querySelector('input[value=submit]');
const cancel_button = document.querySelector('input[value=submit]');
['btn', 'btn-default'].forEach(cls => {
    submit_button && submit_button.classList.add(cls);
    cancel_button&& cancel_button.classList.add(cls);
})

const tags = document.getElementsByClassName("form-control");
const hide = document.getElementById("hide");

hide && hide.addEventListener("click", function () {
    const submit_button = document.getElementById("submit");
    if (submit_button.style.display === "none") {
        hide.innerHTML = "Cancel";
        submit_button.style.display = "";
        for (let tag = 0; tag < 4; tag++) {
            tags[tag].removeAttribute("readonly");
            tags[tag].removeAttribute("disabled");
        }
    } else {
        hide.innerHTML = "Edit";
        submit_button.style.display = "none";
        for (let tag = 0; tag < 4; tag++) {
            tags[tag].setAttribute("readonly", "");
            tags[tag].setAttribute("disabled", "");
        }
    }
    return false;
})
if (hide) {  // Only apply if, required buttons are present
    for (let p = 0; p < tags.length; p++) {
        tags[p].setAttribute("readonly", "");
        tags[p].setAttribute("disabled", "");
    }
}
