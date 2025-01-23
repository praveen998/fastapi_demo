

async def create_new_html(msg):
    htmlcode="""
    """
    for i in msg:
        prod=[]
        for key,value in i.items():
           prod.append(value)

        htmlcode+=f""" 
                <div class="col">
                            <div class="card h-100 shadow-sm"> <img id="product_image"
                                    src="https://www.freepnglogos.com/uploads/notebook-png/download-laptop-notebook-png-image-png-image-pngimg-2.png"
                                    class="card-img-top" alt="...">
                                <div class="card-body">
                                    <div class="clearfix mb-3"> <span class="float-start badge rounded-pill bg-primary" id="product_name">{prod[0]}
                                            </span> <span class="float-end price-hp" id="product_price">{prod[2]}₹</span> </div>
                                    <h5 class="card-title" id="product_description">{prod[1]}</h5>
                                   <div class="text-center my-4"> <a href="" class="btn btn-warning" id="buynow">Buy Now</a> </div>
                                   <div class="text-center my-4"> <a href="" class="float-end price-hp" style="text-decoration: none;" id="addcart" >Add To Cart</a> </div>
                               
                                </div>
                            </div>
                </div>

            """
    return htmlcode