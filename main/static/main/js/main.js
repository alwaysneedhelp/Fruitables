(function functioner() {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow');
            } else {
                $('.fixed-top').removeClass('shadow');
            }
        } else {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow').css('top', -55);
            } else {
                $('.fixed-top').removeClass('shadow').css('top', 0);
            }
        } 
    });
    
    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:1
            },
            992:{
                items:2
            },
            1200:{
                items:2
            }
        }
    });


    // vegetable carousel
    $(".vegetable-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            },
            1200:{
                items:4
            }
        }
    });


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
        
        
    });



    // Product Quantity
    $('.quantity button').on('click', function() {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });

    $(document).ready(function(){
        $('.add-to-cart-btn').on('click', function(){
    
            let this_val = $(this)
            let index = this_val.attr('data-index')
    
            let quantity = $('.product-quantity-' + index).val()
            let product_title = $('.product-title-' + index).val()
            let product_id = $('.product-id-' + index).val()
            let product_price = $('.product-price-' +index).text()
            let product_pid = $('.product-pid-' + index).val()
            let product_image = $('.product-image-' + index).val()
    
            console.log('Index:', index);
            console.log('Quantity:', quantity);
            console.log('Title:', product_title);
            console.log('ID:', product_id);
            console.log('Price:', product_price);
            console.log('PID:', product_pid);
            console.log('Image:', product_image);
            console.log('Current Element:', this_val);
    
            $.ajax({
                url: '/shop/add-to-cart/',
                data: {
                    'id' : product_id,
                    'pid' : product_pid,
                    'image' : product_image,
                    'qty': quantity,
                    'title' : product_title,
                    'price' : product_price,
                },
                dataType: 'json',
                beforeSend: function(){
                    console.log('Adding Product To Cart...');
                },
                success: function(res){
                    this_val.html('✔️');
                    console.log('Added Product To Cart');
                    $('#cart-product-count').text(response.totalcartitems)
                }
            })
        });
    
        $('.delete-product').on('click', function(){
            let product_id = $(this).attr('data_item')
            let this_val = $(this)
            let form_fields_data = $('#field_datas').serializeArray();
            let form_fields = JSON.stringify(form_fields_data);
    
    
            console.log('Product ID:', product_id);
    
            $.ajax({
                url: '/shop/delete_from_cart',
                data: {
                    'id' : product_id,
                    'form_fields': form_fields
                },
                dataType: 'json',
                beforeSend: function(){
                    this_val.hide()
                },
                success: function(response){
                    this_val.show()
                    $('#cart-product-count').text(response.totalcartitems)
                    $('#cart-list').html(response.data)
                    functioner()
                }
            })
        });
    
        $('.update-product').on('click', function(){
            let product_id = $(this).attr('data_item')
            let this_val = $(this)
            let product_qty = $('.product-qty-'+product_id).val()
            let form_fields_data = $('#field_datas').serializeArray();
            let form_fields = JSON.stringify(form_fields_data);

            console.log('Product ID:', product_id);
    
            $.ajax({
                url: '/shop/update_cart',
                data: {
                    'id' : product_id,
                    'qty' : product_qty,
                    'form_fields': form_fields
                },
                dataType: 'json',
                success: function(response){
                    $('#cart-list').html(response.data);
                    $('#cart-product-count').text(response.totalcartitems);
                    functioner()
                },
            })
        });

        $('.qty-input').on('change', function(){
            let product_id = $(this).attr('data_item')
            let this_val = $(this)
            let product_qty = $('.product-qty-'+product_id).val()
            let form_fields_data = $('#field_datas').serializeArray();
            let form_fields = JSON.stringify(form_fields_data);
        
    
            console.log('Product ID:', product_id);
    
            $.ajax({
                url: '/shop/update_cart',
                data: {
                    'id' : product_id,
                    'qty' : product_qty,
                    'form_fields': form_fields
                },
                dataType: 'json',
                success: function(response){
                    $('#cart-list').html(response.data);
                    $('#cart-product-count').text(response.totalcartitems);
                    console.log($('.update-product'));
                    functioner()
                },
            })
        });
        
    });

})(jQuery);

let stars = Array.from(document.querySelectorAll("input"));

stars.forEach((element) => {
  element.addEventListener("click", (e) => {
    rate(element);
  });

  element.addEventListener("mouseover", (e) => {
    rate(element);
  });

});

function rate(element) {
  stars.forEach((el) => {
    el.classList.remove("text-secondary");
  });
  selectedRating = stars.indexOf(element);
  for (let i = 0; i <= selectedRating; i++) {
    stars[i].classList.add("text-secondary");
  }
};

//Add to cart functionality