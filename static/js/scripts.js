$(document).ready(function() {
    $('a[href^="#"]').on('click', function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top
        }, 800);
    });

    $('#contact-form').on('submit', function(e) {
        e.preventDefault();
        
        $('#form-message').text('Mensaje enviado con éxito. Gracias por contactarnos.').fadeIn();
        
        $(this).trigger('reset');
        
        setTimeout(function() {
            $('#form-message').fadeOut();
        }, 5000);
    });

    $('.service').hover(
        function() {
            $(this).css('transform', 'translateY(-5px)');
            $(this).css('box-shadow', '0 5px 15px rgba(0,0,0,0.1)');
        },
        function() {
            $(this).css('transform', 'translateY(0)');
            $(this).css('box-shadow', 'none');
        }
    );
    $('.inline-login input').focus(function() {
        $(this).css('border-color', '#3498db');
    }).blur(function() {
        $(this).css('border-color', '#ddd');
    });

    $('.show-password').click(function() {
        const passwordField = $(this).siblings('input');
        const type = passwordField.attr('type') === 'password' ? 'text' : 'password';
        passwordField.attr('type', type);
        $(this).toggleClass('fa-eye fa-eye-slash');
    });


    $('.card').hover(
        function() {
            $(this).css('transform', 'translateY(-5px)');
            $(this).css('box-shadow', '0 5px 20px rgba(0,0,0,0.15)');
        },
        function() {
            $(this).css('transform', 'translateY(0)');
            $(this).css('box-shadow', '0 2px 15px rgba(0,0,0,0.1)');
        }
    );

    $('.add-to-cart').click(function() {
        const platoId = $(this).data('plato-id');
        alert(`Plato ${platoId} agregado al carrito`);
    });

});