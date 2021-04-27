const loader = document.getElementById("quickloader");

const incdecbuttons = document.querySelectorAll('td>a[role=button]')
function changeValue(e){
    e.preventDefault();
    const itemId = this.classList[0].slice(2,);
    const price = document.querySelector(`#row${itemId}>td:nth-child(3)`).textContent;
    loader.style.display = "block";
    fetch(this.href)
        .then(response=>response.json())
        .then(response=>{
            if(response["quantity"]===0){document.querySelector(`#row${itemId}`).remove()}
            else{
                document.querySelector(`span#sc${itemId}`).textContent = response["quantity"];
                const total = Math.round(response['quantity']*price*100)/100;
                document.querySelector(`#row${itemId}>.total`).textContent = String(total);
            }
            loader.style.display = "none";
            aggregate()
        })
        .catch(_=>{
            loader.style.display = 'none';
            aggregate();
        });
}

const aggregate = _ => {
    const quantities = document.querySelectorAll('.quantity');
    const costs = document.querySelectorAll('.total');
    const agg = document.querySelector('#aggregate');

    agg.querySelector('td:nth-child(2)').textContent = String(Array.from(quantities)
        .reduce((sum, i)=>sum+parseFloat(i.textContent), 0))

    const total = String(Array.from(costs)
        .reduce((sum, i)=>sum+parseFloat(i.textContent), 0))
    agg.querySelector('td:nth-child(4)').textContent = String(Math.round(total*100)/100)
}

window.addEventListener('load', function(){
    incdecbuttons.forEach(button=>{
        button.addEventListener('click', changeValue);
    })
    aggregate();
})
