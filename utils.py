

async def create_new_html(old_code,Perfumes_details):
    htmlcode=f"""
            <div class="col-md-4">
                <div class="card p-3 card-item">
                    <div class="d-flex flex-row mb-3"><br>
                        <img src="/static/images/first.png" width="70"><br>
                        <div class="d-flex flex-column ml-2"><span>{Perfumes_details.perfumes_name}</span><span class="text-black-50">perfume details:{Perfumes_details.perfumes_description}</span><span>price:{Perfumes_details.perfumes_price}</span><span class="ratings"><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i></span></div>
                    </div>
                </div>
            </div>
        """
    htmlcode+=old_code
    return htmlcode