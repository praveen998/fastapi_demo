


$(document).ready(function () {
   
append_cart_items();
    //retrieve_buynow_storage()
    $('#max').click(function () {
        c=maxize_price();
        $("#count").text(`${c}`);
    });


    $('#min').click(function () {
        c=minimize_price();
        $("#count").text(`${c}`);
    });


    $(document).on('click', '#max', function () {

        // const parent = $(this).closest('.cart-item'); // Find the parent item
        // const id = parent.data('id'); // Get the item ID
        // const item = cart.find(item => item.id === id); // Find the item in the cart array

        // if (item) {
        //     item.quantity++; // Increase the quantity
        //     parent.find('.count-display').text(item.quantity); // Update the count display
        //     parent.find('.qty-display').text(item.quantity); // Update the Qty text
        // }
        c=maxize_price();
        const parent = $(this).closest('#count');
        parent.text(`${c}`);
    });


       // Event delegation for Decrease button
       $(document).on('click', '#min', function () {
        // const parent = $(this).closest('.cart-item'); // Find the parent item
        // const id = parent.data('id'); // Get the item ID
        // const item = cart.find(item => item.id === id); // Find the item in the cart array

        // if (item && item.quantity > 1) { // Ensure quantity doesn't go below 1
        //     item.quantity--; // Decrease the quantity
        //     parent.find('.count-display').text(item.quantity); // Update the count display
        //     parent.find('.qty-display').text(item.quantity); // Update the Qty text
        // }
        c=minimize_price();
        const parent = $(this).closest('#count');
        parent.text(`${c}`);
    });


});




// function retrieve_buynow_storage(){
//     const key = 'buynow_product';
//     const storedValue = localStorage.getItem(key);
//     if (storedValue) {
//         let parsedValue = JSON.parse(storedValue);

//         // Alter each data field
     
        
//        // Increase price by 5
//         alert('Product Name: ' +  parsedValue.product_name  + '\n' +
//             'Image Source: ' + parsedValue.product_src + '\n' +
//             'Description: ' + parsedValue.product_description  + '\n' +
//             'Price: ' + parsedValue.product_price);

//     } else {
//         console.log(`${key} does not exist.`);
//     }

// }

function minimize_price(){
    const key = 'buynow_product';
    const product = JSON.parse(localStorage.getItem(key));
    if (product.product_count != 1)
    {
        product.product_count -=1;
    }

    localStorage.setItem(key, JSON.stringify(product));
    return product.product_count;
}


function maxize_price(){
    const key = 'buynow_product';
    const product = JSON.parse(localStorage.getItem(key));
    product.product_count +=1;
    localStorage.setItem(key, JSON.stringify(product));
    return product.product_count;
}

function geturl(){
    url=localStorage.getItem("fasturl");
    return url;
}

let cart=[];

function loadCart() {
    const storedCart = localStorage.getItem('mycart');
    cart = storedCart ? JSON.parse(storedCart) : [];
}


function append_cart_items() {
    loadCart();
    let itemHtml = ""; // Initialize empty HTML string

    for (let i = 0; i < cart.length; i++) {
       // const item = cart[i]; // Access the item at the current index

        // Generate HTML for each cart item
        // itemHtml += `
        // <div class="row align-items-center mb-3">
        //     <div class="col-4 text-center">
        //         <img src="${item.image}" alt="${item.name}" class="rounded-3" style="width: 100%;">
        //     </div>
        //     <div class="col-8">
        //         <span class="mb-0 text-price d-block">$${item.price}</span>
        //         <p class="mb-0">${item.name}</p>
        //         <span>${item.color}</span> <span>${item.size}</span>
        //         <div class="d-flex align-items-center mt-3">
        //             <button class="btn btn-primary btn-sm me-2" onclick="increaseQuantity(${i})">Increase</button>
        //             <div id="count-${i}">${item.quantity}</div>
        //             <button class="btn btn-secondary btn-sm ms-2" onclick="decreaseQuantity(${i})">Decrease</button>
        //         </div>
        //         <p class="mt-2">Qty: <span id="qty-${i}">${item.quantity}</span></p>
        //     </div>
        // </div>
        // `;
        const item = cart[i];
            itemHtml += `
                            <div class="row align-items-center">
                                <div class="col-4 text-center">
                                    <img src=${item.product_src} alt="Blue Jeans Jacket" class="rounded-3">
                                </div>
                                <div class="col-8">
                                    <span class="mb-0 text-price d-block">${item.product_price}</span>
                                    <p class="mb-0">${item.product_name}</p>
                                    <span>Black</span> <span>${item.product_description}</span>
                                    <div class="d-flex align-items-center mt-3">
                                        <button id="max" class="btn btn-primary btn-sm me-2">Increase</button>
                                        <div class="me-2" id="count">1</div>
                                        <button id="min" class="btn btn-secondary btn-sm">Decrease</button>
                                    </div>
                                    <p class="mt-2">Qty: <span>1</span></p>
                                </div>
                            </div>
            `;

        }

        // Inject the generated HTML into the container with ID 'carditems'
        $("#carditems").html(itemHtml);
    }


  