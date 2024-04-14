// cart.js
$(document).ready(function() {
    // Function to update cart count
function updateCartCount() {
    $.ajax({
        url: 'cart/count/',
        type: 'GET',
        success: function(data) {
            $('.cart-count').text(data.cart_count);
        }
    });
    }
    updateCartCount();
});


function addToCart(productId) {
    console.log("Adding product to cart:", productId);
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    var requestData = {
      'product_id': productId,
      'csrfmiddlewaretoken': csrftoken
    };
    $.ajax({
    type: 'POST',
    url: "/add-to-cart/",
    data: requestData,
    dataType: 'json',
    success: function(data) {


    alert(data.message);

    console.log("Cart count:", data.cart_count);
    },
    error: function(xhr, textStatus, errorThrown) {
    console.error("Error:", errorThrown);
    }
});
}