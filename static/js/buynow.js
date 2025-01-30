
function geturl(){
    url=localStorage.getItem("fasturl");
    return url;
}

$(document).ready(function () {
    
    append_cart_item();

    //retrieve_buynow_storage()
    $('#max').click(function () {
        c=maxize_price();
        $("#count").text(`${c}`);
    });


    $('#min').click(function () {
        c=minimize_price();
        $("#count").text(`${c}`);
    });

    var countries = [
        { id: "US", text: "United States" },
        { id: "CA", text: "Canada" },
        { id: "GB", text: "United Kingdom" },
        { id: "IN", text: "India" },
        { id: "AU", text: "Australia" },
        { id: "DE", text: "Germany" },
        { id: "FR", text: "France" },
        { id: "IT", text: "Italy" },
        { id: "ES", text: "Spain" },
        { id: "MX", text: "Mexico" },
        // Add more countries here as needed
    ];

    // Populate the country dropdown using the static list
    var countrySelect = $('#country');
    countries.forEach(function(country) {
        countrySelect.append('<option value="' + country.id + '">' + country.text + '</option>');
    });

});




function retrieve_buynow_storage(){
    const key = 'buynow_product';
    const storedValue = localStorage.getItem(key);
    if (storedValue) {
        let parsedValue = JSON.parse(storedValue);
        alert('Product Name: ' +  parsedValue.product_name  + '\n' +
            'Image Source: ' + parsedValue.product_src + '\n' +
            'Description: ' + parsedValue.product_description  + '\n' +
            'Price: ' + parsedValue.product_price);

    } else {
        console.log(`${key} does not exist.`);
    }

}

function minimize_price(){
    const key = 'buynow_product';
    const product = JSON.parse(localStorage.getItem(key));
    if (product.product_count != 1)
    {
        product.product_count -=1;
        product.product_total -=product.product_price;
        $("#subtotal").text(`${product.product_total}`);
        $("#total").text(`${product.product_total}`);
    }
    localStorage.setItem(key, JSON.stringify(product));
    return product.product_count;
}


function maxize_price(){
    const key = 'buynow_product';
    const product = JSON.parse(localStorage.getItem(key));
    product.product_count +=1;
    product.product_total +=product.product_price;
    $("#subtotal").text(`${product.product_total}`);
    $("#total").text(`${product.product_total}`);
    localStorage.setItem(key, JSON.stringify(product));
    return product.product_count;
}


function append_cart_item(){
    const key = 'buynow_product';
    const storedValue = localStorage.getItem(key);
    if (storedValue) {
        let parsedValue = JSON.parse(storedValue);
        $("#subtotal").text(`${parsedValue.product_total}`);
        $("#total").text(`${parsedValue.product_total}`);
        
        // alert('Product Name: ' +  parsedValue.product_name  + '\n' +
        //     'Image Source: ' + parsedValue.product_src + '\n' +
        //     'Description: ' + parsedValue.product_description  + '\n' +
        //     'Price: ' + parsedValue.product_price);
        carditem=`
                        <div class="row align-items-center">
                            <div class="col-4 text-center">
                                <img  src=${parsedValue.product_src}
                                alt="Blue Jeans Jacket" class="rounded-3">
                            </div>
                            <div class="col-8">
                                <span class="mb-0 text-price d-block">${parsedValue.product_price}</span>
                                <p class="mb-0"><b>${parsedValue.product_name}</b></p>
                                <span>Black</span> <span>${parsedValue.product_description}</span>
                                <div class="d-flex align-items-center mt-3">
                                    <button id="max" class="btn btn-primary btn-sm me-2">+</button>
                                    <div id="count">1</div>
                                    <button id="min" class="btn btn-secondary btn-sm ms-2">-</button>
                                </div>
                            </div>
                        </div>
                        </div>

                        
            
                        
    `
    $("#card_item").html(carditem);

    } else {
        console.log(`${key} does not exist.`);
    }
    
}


function retrieve_buynow_storage(){
    const key = 'buynow_product';
    const storedValue = localStorage.getItem(key);
    if (storedValue) {
        let parsedValue = JSON.parse(storedValue);
        alert('Product Name: ' +  parsedValue.product_name  + '\n' +
            'Image Source: ' + parsedValue.product_src + '\n' +
            'Description: ' + parsedValue.product_description  + '\n' +
            'Price: ' + parsedValue.product_price);

    } else {
        console.log(`${key} does not exist.`);
    }

}

