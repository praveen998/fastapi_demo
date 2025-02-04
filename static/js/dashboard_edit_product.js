function geturl() {
    url = localStorage.getItem("fasturl");
    return url;
}




$(document).ready(function () {
   
$(document).on("change", ".edit_product_category", function () {
    const selectedValue = $(this).val(); // Get the selected value
    //alert(`${selectedValue}`);
    loadTable(selectedValue);
    // $.ajax({
    //     url: geturl() + "/list_products/",
    //     type: "POST",
    //     contentType: "application/json",
    //     data: JSON.stringify(data),
    //     success: function (response) {
    //         alert('product change');
    //     },
    //     error: function (xhr, status, error) {
    //         console.error("Error fetching text:", error);
    //         $('#textContent').text("Error fetching text. Please try again.");
    //     }
    // });

});



$(document).on("click", ".save", function() {
    let row = $(this).closest("tr");
    let id = row.data("id");
    let name = row.find(".name").val();
    let desc = row.find(".desc").val();
    let price;
    alert(`${name}`);
    try {
        price = JSON.parse(row.find(".price").val());
    } catch (e) {
        alert("Invalid JSON format in price field");
        return;
    }
    let image = row.find(".image-upload")[0].files[0];
    let imagePath = products[id][3];

    if (image) {
        let reader = new FileReader();
        reader.onload = function(e) 
        {
            row.find("img").attr("src", e.target.result);
            products[id] = [name, desc, price, e.target.result];
            alert("Product updated successfully!");
        };
        reader.readAsDataURL(image);
    } 
    else {
        products[id] = [name, desc, price, imagePath];
        alert("Product updated successfully!");
    }
});


$(document).on("click", ".delete", function() {
    let row = $(this).closest("tr");
    let name = row.find(".name").val();
    alert(`${name}`);
    
});



});




//let products = {"1":["vanila perfume 50ml","good body perfume",{"UAE":111.0,"India":555.0},"https://nibhasitsolutions.s3.ap-south-1.amazonaws.com/kali-linux-3840x2160-18058.jpg"],"2":["rose perfume 100ml","good body perfume",{"UAE":222.0,"India":444.0},"kali-linux-3840x2160-18058.jpg"],"3":["jasmin perfume","very smelly body perfume...",{"UAE":99.0,"India":111.0},"kali-linux-3840x2160-18058.jpg"],"4":["oarchid perfume","nice perfume",{"UAE":22.0,"India":333.0},"kali-linux-3840x2160-18058.jpg"]};

function loadTable(data) {
    let products=null;
    const token = sessionStorage.getItem("jwt");
   
     $.ajax({
            url: geturl()+"/list_products_edit_product/",
            type: "POST",
            headers: {
                "Authorization": "Bearer " + token
            },
            contentType: "application/json",
            data: JSON.stringify({ category: data }),
            success: function (response) {
               products=response;
               let tbody = "";
               $.each(products, function(key, product) {
                   tbody += `<tr data-id="${key}">
                       <td><input type="text" class="form-control name" value="${product[0]}"></td>
                       <td><textarea class="form-control desc">${product[1]}</textarea></td>
                       <td><textarea class="form-control price">${JSON.stringify(product[2])}</textarea></td>
                       <td class="text-center">
                           <img src="${product[3]}" class="img-thumbnail" alt="Product Image">
                           <input type="file" class="form-control image-upload mt-2" accept="image/*">
                       </td>   
                       <td class="text-center">
                           <button class="btn btn-success save">Save</button>
                           <button class="btn btn-danger delete">Delete</button>
                       </td>
                   </tr>`;
               });
           
               $("#productTable tbody").html(tbody);
            },
            error: function (xhr, status, error) {
                console.error("Error fetching text:", error);
                alert("Error fetching text. Please try again.");
            }
        });

   
}

