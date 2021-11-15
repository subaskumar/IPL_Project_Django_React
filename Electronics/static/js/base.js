/* for add quantity of product */

function quantity_inc(quantity_input) {
    if(document.getElementById(quantity_input).value > 0){
        document.getElementById(quantity_input).value = parseInt(document.getElementById(quantity_input).value) + 1
    }
}
function quantity_dec(quantity_input) {
    if(document.getElementById(quantity_input).value >= 2){
        document.getElementById(quantity_input).value = parseInt(document.getElementById(quantity_input).value) - 1
    }
}

$(document).ready(function() {

    var otpverify = document.getElementById("VerificationOTP")
    var otpsent = document.getElementById("OTPsentForm")
    var x = document.getElementById("snackbar")


    $('.modal').find(':input').focus(function(){
        var label = $('label[for="' + $(this).attr('id') + '"]');
        $(label).css({"transform": "translateY(12px)", "font-size" : "13px"});
        $(this).css("border-bottom", "1px solid #2874f0");
    });
    $('.modal').find(':input').blur(function(){
        var label = $('label[for="' + $(this).attr('id') + '"]');
        if ($(this).val().length <= 0){
            $(this).css("border-bottom", "1px solid rgb(170, 168, 168)");
            $(label).css({"transform": "translateY(30px)", "font-size" : "16px"});
              /*  if($(".modal").css("display") == 'none'){
                    alert("ok")
                    $(label).css({"transform": "translateY(40px)", "font-size" : "16px"});
                    } */
        }
    });

  
  // ajax OTP send 
  $('#verifyphone').submit(function(event){
    event.preventDefault()

    var x = document.getElementById("snackbar");
    const url = $(this).attr('action')
    var serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: url,
        data: serializedData,
        dataType: 'json',
        success: function(response) {
           /* if(Object.keys(response.errorform).length >= 1) */
            if(response.errorform.phone){
                $("#phoneError").text(response.errorform.phone);
                $("#phone").css("border-bottom", "2px solid red");
            }
            else if(response.message == "Sucessfully"){
                
                x.className = "show";
                x.innerHTML = "<i class='fa fa-check-circle'></i>  Verification code sent to " + response.phone;
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
                otpsent.style.display = "none";
                otpverify.style.display = "block";
                document.getElementById("phoneRegister").value = response.phone
            }
            else{
                alert("We are Unable to sent OTP to " + response.phone )
            }
        },                        
        error:function(response) {
            x.className = "show";
            x.innerHTML = "<i class='fa fa-exclamation-circle'></i>  Something's not right. Please try again.";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
        }
    });
  });


  // Ajax registration form

  $('#verifyotp').submit(function(event){
    event.preventDefault()

    const url = $(this).attr('action')
    var serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: url,
        data: serializedData,
        dataType: 'json',
        success: function(response) {
            if(response.message == "Wrong OTP"){
                $("#OtpError").text("Please enter valid OTP");
                $("#otp").css("border-bottom", "2px solid red");
            }
            else if(response.registererror.phone){
                $("#phoneRegisterError").text(response.registererror.phone);
                $("#phoneRegister").css("border-bottom", "2px solid red");
                
            }
            else if(response.registererror.password1){
                $("#passwordError").text(response.registererror.password1);
                $("#password").css("border-bottom", "2px solid red");
                
            }
            else if(response.registererror.password2){
                $("#confirmPasswordError").text(response.registererror.password2);
                $("#conformpassword").css("border-bottom", "2px solid red");
                
            }
            else if(response.message == 'UserRegistered') {
                // showModal(modallogin)
                
                x.className = "show";
                x.innerHTML = "<i class='fa fa-check-circle'></i>  You Registred Successfully  ";
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
                $(".register").trigger('reset');
                document.getElementById("SignUpModal").style.display = 'none';
                document.getElementById("LoginModal").style.display = 'block'


            }
            },
        error:function(response) {
            x.className = "show";
            x.innerHTML = "<i class='fa fa-exclamation-circle'></i>  Something's not right. Please try again.";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
            
        }
    });
  });


  // Ajax Login form

  $('#Loginform').submit(function(event){
    event.preventDefault()

    const url = $(this).attr('action')
    var serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: url,
        data: serializedData,
        dataType: 'json',
        success: function(response) {
            if(response.formerror.phone){
                $("#phoneLoginError").text(response.formerror.phone);
                $("#phoneLogin").css("border-bottom", "2px solid red");
                
            }
            else if(response.formerror.password){
                $("#passwordLoginError").text(response.formerror.password);
                $("#passwordLogin").css("border-bottom", "2px solid red");
                
            }
            else if(response.message == 'loginSucessfully'){
                x.className = "show";
                x.innerHTML = "<i class='fa fa-check-circle'></i>  Logged in Successfully  ";
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 1000);
                $(".register").trigger('reset');
                document.getElementById("LoginModal").style.display = 'none'
                window.location.reload()

            }
            else if(response.message == 'invalidForm'){
                x.className = "show";
                x.innerHTML = "<i class='fa fa-exclamation-circle'></i>  Your account is Deactivated, Please active it.";
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
            }
        },
        error:function(response) {
            x.className = "show";
            x.innerHTML = "<i class='fa fa-exclamation-circle'></i>  Something's not right. Please try after 24hr.";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
            
        }
    });
  });

    $('#add_item_cart').submit(function(event){
        event.preventDefault()
        var cart_item = $('#add_cart_item').text()
        const url = $(this).attr('action')
        var serializedData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: url,
            data: serializedData,
            dataType: 'json',
            success: function(response) {
            /* if(Object.keys(response.errorform).length >= 1) */
                if(response.message == 'item_added'){
                    x.className = "show";
                    x.innerHTML = "<i class='fa fa-check-circle'></i>" + response.quantity+ "item " + response.product + " Added to your Cart";
                    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
                    $('#add_cart_item').css('visibility','visible')
                    $('#add_cart_item').text(parseInt(cart_item) + 1)
                }
                if(response.message == 'already_exit'){
                    x.className = "show";
                    x.innerHTML = "<i class='fa fa-check-circle'></i> This item Already Added to your Cart";
                    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);

                }
            },                        
            error:function(response) {
                x.className = "show";
                x.innerHTML = "<i class='fa fa-exclamation-circle'></i>  Something's not right. Please try again.";
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
            }
        });
    });





  // for Product menu
    $('.product-menu').slick({
      dots: false,
      loop: true,
      autoplay: false,
      arrows: false,
      slidesToShow: 9,
      infinite: true,
      swipeToSlide: true,
      slidesToScroll: 9,
        responsive: [
            {
            breakpoint: 1024,
            settings: {
            slidesToShow: 7
            }
            },
        {
          breakpoint: 800,
          settings: {
            slidesToShow: 5
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 4
          }
        },
        
        {
          breakpoint: 450,
          settings: {
            slidesToShow: 3
          }
        }
      ]   
    });


    /* for slider */
  $('.slider').each(function() {
    var $this = $(this);
    var $group = $this.find('.slide_group');
    var $slides = $this.find('.slide');
    var bulletArray = [];
    var currentIndex = 0;
    var timeout;
    
    function move(newIndex) {
        var animateLeft, slideLeft;
        
        advance();
        
        if ($group.is(':animated') || currentIndex === newIndex) {
        return;
        }
        
        bulletArray[currentIndex].removeClass('active');
        bulletArray[newIndex].addClass('active');
        
        if (newIndex > currentIndex) {
        slideLeft = '100%';
        animateLeft = '-100%';
        } else {
        slideLeft = '-100%';
        animateLeft = '100%';
        }
        $slides.eq(newIndex).css({
        display: 'block',
        left: slideLeft
        });
        $group.animate({
        left: animateLeft
        }, function() {
        $slides.eq(currentIndex).css({
            display: 'none'
        });
        $slides.eq(newIndex).css({
            left: 0
        });
        $group.css({
            left: 0
        });
        currentIndex = newIndex;
        });
    }
    function advance() {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
        if (currentIndex < ($slides.length - 1)) {
            move(currentIndex + 1);
        } else {
            move(0);
        }
        }, 6000);
    }
    $('.next_btn').on('click', function() {
        if (currentIndex < ($slides.length - 1)) {
        move(currentIndex + 1);
        } else {
        move(0);
        }
    }); 
    $('.previous_btn').on('click', function() {
        if (currentIndex !== 0) {
        move(currentIndex - 1);
        } else {
        move(3);
        }
    });
    $.each($slides, function(index) {
        var $button = $('<a class="slide_btn">&bull;</a>');
        
        if (index === currentIndex) {
        $button.addClass('active');
        }
        $button.on('click', function() {
        move(index);
        }).appendTo('.slide_buttons');
        bulletArray.push($button);
    });
    advance();
    });

});


  