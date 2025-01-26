
seturl()
const CART_KEY = "globalCart";
$.ajax({
    url: geturl()+"/list_category",
    method: "GET",
    success: function (data) {
        const selectElement = $("#styledSelect");
        selectElement.empty(); // Clear existing options
           // Add new options dynamically
           data.forEach(option => {
            selectElement.append(
                `<option value="${option.categories}">${option.categories}</option>`
            );
        });
    },
    error: function () {
        alert("Failed to load options. Please try again.");
    }
});

$('#buy-now-btn').click(function(e) {
    //e.preventDefault();  // Prevent the default action of the link
    //var productTitle = $(this).closest('.card-body').find('.card-title').text();  // Get the text of the card-title
    //alert("You selected: " + productTitle);  // Show alert with the product title
    alert('hai');

});

$('#buynow').click(function(){
    alert('buy now');
});

$(document).ready(function () {
  
const data = {"category": "body perfumes"};

$.ajax({
    url: geturl()+"/list_products/", // Update URL if hosted elsewhere
    method: "POST",
    contentType: "application/json",
    data:JSON.stringify(data),
    success: function (data) {
        // Append fetched text to the div
        $('#grid-container').html(data);

        $('#grid-container').on('click', '#buynow', function(e) {
            e.preventDefault();
            var closestCard = $(this).closest('.card');
            var productName = closestCard.find('[id^="product_name"]').text();
            var productImageSrc = closestCard.find('[id^="product_image"]').attr('src');
            var productDescription = closestCard.find('[id^="product_description"]').text();
            var productPrice = closestCard.find('[id^="product_price"]').text();
            var productPrice = parseInt(productPrice.replace(/[₹,]/g, '')); 
            create_buynow_storage(productName,productImageSrc,productPrice,productDescription)
            window.location.href = geturl()+"/buynow";
            
          
        });

        $('#grid-container').on('click', '#addcart', function(e) {
            e.preventDefault()
            var closestCard = $(this).closest('.card');
            var productName = closestCard.find('[id^="product_name"]').text();
            var productImageSrc = closestCard.find('[id^="product_image"]').attr('src');
            var productDescription = closestCard.find('[id^="product_description"]').text();
            var productPrice = closestCard.find('[id^="product_price"]').text();
            var productPrice = parseInt(productPrice.replace(/[₹,]/g, '')); 

            let cart = getCart();
            let product = {
                product_name: productName,
                product_image: productImageSrc,
                product_description: productDescription,
                product_price: productPrice,
                product_quantity: 1 // Default quantity is 1
            };
                 // Check if the product already exists in the cart
            let existingProduct = cart.find(item => item.name === product.name);
            if (existingProduct) {
                // If product exists, increase quantity
                existingProduct.quantity += 1;
            } else {
                // Add new product to cart
                cart.push(product);
            }

            saveCart(cart);
            const cartDetails = formatCartDetails(cart);
            alert(cartDetails);

            //window.location.href = geturl()+"/buynow";
               
        });


    },
    error: function (xhr, status, error) {
        console.error("Error fetching text:", error);
        $('#textContent').text("Error fetching text. Please try again.");
    }
});

 


//submit selection boc category to backend------------------------------------
$("#styledSelect").on("change", function () {
    const selectedValue = $(this).val(); // Get the selected value
    // Prepare data to send
    const data = {"category": selectedValue};

    // Send data to the backend using AJAX
    $.ajax({
        url: geturl()+"/list_products/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
            $('#grid-container').html(response);

            $('#grid-container').on('click', '#buynow', function(e) {
                e.preventDefault();
                var closestCard = $(this).closest('.card');
                var productName = closestCard.find('[id^="product_name"]').text();
                var productImageSrc = closestCard.find('[id^="product_image"]').attr('src');
                var productDescription = closestCard.find('[id^="product_description"]').text();
                var productPrice = closestCard.find('[id^="product_price"]').text();
                var productPrice=parseInt(productPrice.replace(/[₹,]/g, ''));
                create_buynow_storage(productName,productImageSrc,productPrice,productDescription)
                window.location.href = geturl()+"/buynow";
          
           
               // retrieve_buynow_storage();
          
            });

            $('#grid-container').on('click', '#addcart', function(e) {
                e.preventDefault();
                var closestCard = $(this).closest('.card');
                var productName = closestCard.find('[id^="product_name"]').text();
                var productImageSrc = closestCard.find('[id^="product_image"]').attr('src');
                var productDescription = closestCard.find('[id^="product_description"]').text();
                var productPrice = closestCard.find('[id^="product_price"]').text();
                var productPrice = parseInt(productPrice.replace(/[₹,]/g, '')); 
                window.location.href = geturl()+"/buynow";
           
            });


        },
        error: function (xhr, status, error) {
            console.error("Error fetching text:", error);
            $('#textContent').text("Error fetching text. Please try again.");
           
        },
    });
});


    // Attach click event to Buy Now button

});


function create_buynow_storage(productname,productsrc,productprice,productdescription){
    const key = 'buynow_product';
    const sampleValue = {
        product_name: productname,
        product_description: productdescription,
        product_price: productprice ,
        product_src : productsrc,
        product_count : 1
    };

    // Check if the key exists
    if (localStorage.getItem(key)) {
        // Remove the existing key
        localStorage.removeItem(key);
        console.log(`${key} key exists. Removing the old entry.`);
    }

    // Create a new key with the sample value
    localStorage.setItem(key, JSON.stringify(sampleValue));
    console.log(`New ${key} created with value:`, sampleValue);


}


// function retrieve_buynow_storage(){
//     const key = 'buynow_product';
//     const storedValue = localStorage.getItem(key);
//     if (storedValue) {
//         let parsedValue = JSON.parse(storedValue);
        
//         // alert('Product Name: ' +  parsedValue.product_name  + '\n' +
//         //     'Image Source: ' + parsedValue.product_src + '\n' +
//         //     'Description: ' + parsedValue.product_description  + '\n' +
//         //     'Price: ' + parsedValue.product_price);

//     } else {
//         console.log(`${key} does not exist.`);
//     }

// }



function seturl(){
    localStorage.setItem("fasturl", "http://127.0.0.1:8000"); 
}

function geturl(){
    url=localStorage.getItem("fasturl");
    return url;
}


function getCart() {
    const cart = localStorage.getItem(CART_KEY);
    return cart ? JSON.parse(cart) : [];
}

function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
}


  // Function to format cart details for alert
  function formatCartDetails(cart) {
    if (cart.length === 0) {
        return "Your cart is empty!";
    }

    let details = "Cart Details:\n";
    cart.forEach((item, index) => {
        details += `\nItem ${index + 1}:\n`;
        details += `Name: ${item.product_name}\n`;
        details += `Description: ${item.product_description}\n`;
        details += `Price: ₹${item.product_price}\n`;
        details += `Quantity: ${item.product_quantity}\n`;
    });
    return details;
}
