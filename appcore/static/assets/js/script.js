mobile_brand_links = $('#mobile-list > div > div > div.category-sidebar > ul > li')
tablet_brand_links = $('#tablet-list > div > div > div.category-sidebar > ul > li')
mobile_link_full = $("#mobile-list > div > div > div.category-detail > a")[0]
tablet_link_full = $("#tablet-list > div > div > div.category-detail > a")[0]
mobile_category_container = $('#mobile-list > div > div')[0]
tablet_category_container = $('#tablet-list > div > div')[0]
mobile_category_item_full = $('#mobile-list > div > div > div.category-detail > a')[0]
tablet_category_item_full = $('#tablet-list > div > div > div.category-detail > a')[0]
var mobile_item_row = $('#mobile-list > div > div > div.category-detail > div > div')[0]
var tablet_item_row = $('#tablet-list > div > div > div.category-detail > div > div')[0]
function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();
  
    // Change this to div.childNodes to support multiple top-level nodes.
    return div.firstElementChild;
  }
for (let i of mobile_brand_links) {
    i.addEventListener("click", (ev) => {
        ev.preventDefault()
        $.ajax(
            {method: "POST",
            url: `${location.origin}/get_brand_products`,
        data: {"brand": ev.target.innerText, "products": "mobile", csrfmiddlewaretoken: csrf_token,}}
        ).done((elems) => {
            products = elems["products"]
            mobile_category_item_full.setAttribute("href", `/${products[0].id}/product_details`)
            mobile_category_item_full.innerHTML = `<div class="item">
            <div class="item-cover">
                <img src="/static${products[0].image_path}" alt="">
            </div>
            <div class="item-info bottom">
                <h4 class="item-title">${products[0].product_name}</h4>
                <p class="item-desc">${products[0].product_tagline}</p>
                <div class="item-price">$${~~(products[0].product_price - (products[0].product_price * (products[0].discount / 100)))}</div>
            </div>
        </div>`            
            products.shift()
            mobile_category_item_list = document.createElement("div")
            mobile_category_item_list.classList += "category-item list"
            mobile_item_row_replacement = document.createElement("div")
            mobile_item_row_replacement.classList += 'item-row'
            for (let i = 0; i < products.length; i++) {
                elem = createElementFromHTML(
                    `<div class="item item-thumbnail">
                    <a href="/${products[i].id}/product_details" class="item-image">
                        <img src="/static${products[i].image_path}" alt="">
                        
                            <div class="discount">${products[i].discount}% OFF</div>
                        
                    </a>
                    <div class="item-info">
                        <h4 class="item-title">
                            <a href="/${products[i].id}/product_details">${products[i].product_name}</a>
                        </h4>
                        <p class="item-desc">${products[i].product_tagline}</p>
                        
                            <div class="item-price">$${~~(products[i].product_price - (products[i].product_price * (products[i].discount / 100)))}</div>
                        
                    </div>
                </div>`
                )
                mobile_item_row_replacement.appendChild(elem)
            }
        mobile_item_row.outerHTML = mobile_item_row_replacement.outerHTML
        mobile_item_row = $('#mobile-list > div > div > div.category-detail > div > div')[0]
        })
    })
}
for (let i of tablet_brand_links) {
    i.addEventListener("click", (ev) => {
        ev.preventDefault()
        $.ajax(
            {method: "POST",
            url: `${location.origin}/get_brand_products`,
        data: {"brand": ev.target.innerText, "products": "tablet", csrfmiddlewaretoken: csrf_token,}}
        ).done((elems) => {
            tablet_category_item_full.setAttribute("href", `/${products[0].id}/product_details`)
            tablet_category_item_full.innerHTML = `<div class="item">
            <div class="item-cover">
                <img src="/static${products[0].image_path}" alt="">
            </div>
            <div class="item-info bottom">
                <h4 class="item-title">${products[0].product_name}</h4>
                <p class="item-desc">${products[0].product_tagline}</p>
                <div class="item-price">$${~~(products[0].product_price - (products[0].product_price * (products[0].discount / 100)))}</div>
            </div>
        </div>`            
            products.shift()
            tablet_category_item_list = document.createElement("div")
            tablet_category_item_list.classList += "category-item list"
            tablet_item_row_replacement = document.createElement("div")
            tablet_item_row_replacement.classList += 'item-row'
            for (let i = 0; i < products.length; i++) {
                elem = createElementFromHTML(
                    `<div class="item item-thumbnail">
                    <a href="/${products[i].id}/product_details" class="item-image">
                        <img src="/static${products[i].image_path}" alt="">
                        
                            <div class="discount">${products[i].discount}% OFF</div>
                        
                    </a>
                    <div class="item-info">
                        <h4 class="item-title">
                            <a href="/${products[i].id}/product_details">${products[i].product_name}</a>
                        </h4>
                        <p class="item-desc">${products[i].product_tagline}</p>
                        
                            <div class="item-price">$${~~(products[i].product_price - (products[i].product_price * (products[i].discount / 100)))}</div>
                        
                    </div>
                </div>`
                )
                tablet_item_row_replacement.appendChild(elem)
            }
        tablet_item_row.outerHTML = tablet_item_row_replacement.outerHTML
        tablet_item_row = $('#tablet-list > div > div > div.category-detail > div > div')[0]
        })
    })
}