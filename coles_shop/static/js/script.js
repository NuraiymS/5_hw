

function func(){
    console.log('Hello world')
}
function set_product_count() {
    const product_span = document.querySelector("#product-count-block")
    product_span.innerHTML = "(20)"
    fetch("/product/count/", init{
        method:'GET'
    }).then(
        (res: Response) => res. json()
    ).then(
        (data)=>{
            product_span.innerHTML(`(${data.count})`)
        }
    )
}


