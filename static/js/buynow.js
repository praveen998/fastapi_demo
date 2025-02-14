
function geturl(){
    url=localStorage.getItem("fasturl");
    return url;
}

function sanitizeInput(input) {
    return $("<div>").text(input).html();
}


$(document).ready(function () {
    append_cart_item();
    $('.placeorder').click(function(){
        let firstName = sanitizeInput($("#firstName").val());
        let lastName = sanitizeInput($("#lastName").val());
        let email = sanitizeInput($('#email').val());
        let country=sanitizeInput($('#country').val());
        let additionalInfo=sanitizeInput($('#additionalInfo').val());

        if(firstName && lastName && email && country && additionalInfo){
        alert(`
            firstname: ${firstName},
            lastName: ${lastName},
            email: ${email},
            country:${country},
            additionalinfo:${lastName}`);
        }
        else{
            $(".required").text('error:fill every field...');
        }
            const key = 'buynow_product';
            const storedValue = localStorage.getItem(key);
            if (storedValue) 
            {
                let parsedValue = JSON.parse(storedValue);
                product_name=parsedValue.product_name;
                product_price=parsedValue.product_price;
                product_count=parsedValue.product_count;
                product_total=parsedValue.product_total;


                // alert(`product_name:${product_name},
                //     product_price:${product_price},
                //     product_count:${product_count},
                //     product_total:${product_total}
                //     `);
            }
        });
    


    

    $("#pay-button").click(async function () {
        // Fetch order details from FastAPI
        let response = await $.ajax({
            url: geturl()+"/create-order/",
            type: "POST",
        });

        let options = {
            "key": "rzp_test_b9S6cM2RxVtasJ",
            "amount": response.amount,
            "currency": "INR",
            "order_id": response.id,
            "handler": async function (razorpayResponse) {
                // Send payment verification data to FastAPI
                let verifyResponse = await $.ajax({
                    url: geturl()+"/verify-payment/",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(razorpayResponse)
                });
                alert(verifyResponse.status);
            }
        };
        let rzp1 = new Razorpay(options);
        rzp1.open();
    });



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
                                <span>${parsedValue.product_description}</span>
                                <div class="d-flex align-items-center mt-3">
                                    <button id="max" class="btn btn-primary btn-sm me-2">+</button>
                                    <div id="count">1</div>
                                    <button id="min" class=" btn btn-secondary btn-sm ms-2">-</button>
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

