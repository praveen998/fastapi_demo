
function geturl(){
    url=localStorage.getItem("fasturl");
    return url;
}


$(document).ready(function () {

    //retrieve_buynow_storage()
    $('#max').click(function () {
        c=maxize_price();
        $("#count").text(`${c}`);
    });


    $('#min').click(function () {
        c=minimize_price();
        $("#count").text(`${c}`);
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
