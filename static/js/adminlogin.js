
function geturl(){
    url=localStorage.getItem("fasturl");
    return url;
}



$(document).ready(function () {
 
   // retrieve_buynow_storage()
});



function retrieve_buynow_storage(){
    const key = 'buynow_product';
    const storedValue = localStorage.getItem(key);
    if (storedValue) {
        let parsedValue = JSON.parse(storedValue);

        // Alter each data field
     
        
       // Increase price by 5
        // alert('Product Name: ' +  parsedValue.product_name  + '\n' +
        //     'Image Source: ' + parsedValue.product_src + '\n' +
        //     'Description: ' + parsedValue.product_description  + '\n' +
        //     'Price: ' + parsedValue.product_price);

    } else {
        console.log(`${key} does not exist.`);
    }

}