const loader = document.getElementById("quickloader");
const page = document.getElementsByTagName("div")[1];

const incdecbuttons = document.querySelectorAll('td>a[role=button]')
function changeValue(e){
    e.preventDefault();
    const itemId = this.classList[1].slice(2,);
    const price = document.querySelector(`#row${itemId}>td:nth-child(3)`).textContent;
    loader.style.display = "block";
    fetch(this.href)
        .then(response=>response.json())
        .then(response=>{
            if(response["quantity"]===0){document.querySelector(`#row${itemId}`).remove()}
            else{
                document.querySelector(`span#sc${itemId}`).textContent = response["quantity"];
                const total = Math.floor(response['quantity']*price*100)/100;
                document.querySelector(`#row${itemId}>.total`).textContent = String(total);
            }
            loader.style.display = "none";
        })
        .catch(_=>{
            loader.style.display = 'none';
        });
}

incdecbuttons.forEach(button=>{
    button.addEventListener('click', changeValue);
})
