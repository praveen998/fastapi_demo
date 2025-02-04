


$(document).ready(function () {
   
append_cart_items();
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

    $(document).on('click', '.remove', function (e) {
        e.preventDefault();
        const productName = $(this).closest('.col-8').find('.pname').text();
        
        const productindex = cart.findIndex(item => item.product_name === productName);
        
        if (productindex !== -1) {
            // Remove the product from the cart array
           // alert(productindex);
            cart.splice(productindex,1);
            saveCart();
           
        } 
        window.location.reload(); 

    });


    $(document).on('click', '.max', function (e) {
        e.preventDefault();
        const productName = $(this).closest('.col-8').find('.pname').text();
        const product = cart.find(item => item.product_name === productName);
      
        if (product){
            product.product_count+=1;
            product.product_total+=product.product_price;
            const count = $(this).closest('.col-8').find('.count');
            count.text(`${product.product_count}`);
            
        }
        saveCart();  
        count_total_price();
       

    });


       // Event delegation for Decrease button
       $(document).on('click', '.min', function (e) {
        e.preventDefault();
        const productName = $(this).closest('.col-8').find('.pname').text(); // Find the product name
         const product = cart.find(item => item.product_name === productName);
         if (product){
            if (product.product_count > 1)
                {
                    product.product_count-=1
                    product.product_total-=product.product_price;
                    const count = $(this).closest('.col-8').find('.count');
                    count.text(`${product.product_count}`);
                    
                }
               
         }
         saveCart();
         count_total_price();
    });


});



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
    count_total_price();
    $(".items").text(`${cart.length} Items`);
    let itemHtml = ""; // Initialize empty HTML string

    for (let i = 0; i < cart.length; i++) {
        const item = cart[i];
            itemHtml += `
                            <div class="row align-items-center">
        
                                <div class="col-4 text-center">
                                    <img src=${item.product_src} alt="Blue Jeans Jacket" class="rounded-3">
                                </div>
                               
                                <div class="col-8">
                
                               
                            
                                    <span class="mb-0 text-price d-block">${item.product_price}</span>
                                    <p class="pname mb-0">${item.product_name}</p>
                                    <span>${item.product_description}</span>
                                    <div class="d-flex align-items-center mt-3">
                                        <button class="max btn btn-primary btn-sm me-2">+</button>
                                         <div class="count mt-2">${item.product_count}</div>
                                        <button class="min btn btn-secondary btn-sm"  style="display: inline-block; margin-left: 1em;">-</button>
                                          <button class="remove float-start badge rounded-pill bg-primary"  style="display: inline-block; margin-left: 5em;">
                                          remove</button>
                                
                                    </div><br>
                                    
                                </div>  
                            </div>
                             
                            <br>
                
            `;

        }

        // Inject the generated HTML into the container with ID 'carditems'
        $("#carditems").html(itemHtml);
    }


    function saveCart() {
        localStorage.setItem('mycart', JSON.stringify(cart));
    }
    

    function count_total_price(){
        let total_price=0;
        // loadCart();
        let itemHtml = ""; // Initialize empty HTML string
    
        for (let i = 0; i < cart.length; i++) {
            const item = cart[i];
            total_price+=item.product_total;
        }
        $("#subtotal").text(`${total_price}`);
        $("#total").text(`${total_price}`);
    }