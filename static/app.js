// Carousel functionality for home page
$('.carousel').carousel({
    interval: 4000,
    pause: "false"
  });

let $item = $('.carousel-item');
let $wHeight = $(window).height();

$item.height($wHeight);
$item.addClass('full-screen');

$('.carousel img').each(function() {
    let $src = $(this).attr('src');
    let $color = $(this).attr('data-color');

    $(this).parent().css({
        'background-image' : 'url(' + $src + ')',
        'background-color' : $color
    });
    $(this).remove();
});

$(window).on('resize', function (){
    $wHeight = $(window).height();
    $item.height($wHeight);
});

$item.eq(0).addClass('active');

//  end of carousel