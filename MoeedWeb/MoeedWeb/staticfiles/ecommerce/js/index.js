document.onreadystatechange = function (e) {
    if (document.readyState === 'complete') {
        if (window.innerWidth > 750)
        {
            $('#carouselExampleIndicators').height(window.innerHeight - 40);
            $('.d-block').height(window.innerHeight - 40);
            console.log();
        }
    }
}

window.onload = function () {
    $('.searchBtn').on('click', () => {
        $('.searchBox').addClass('active');
        $('.search').addClass('active');
    })

    $('.searchBox input').focusout(() => {
        $('.searchBox').removeClass('active');
        $('.search').removeClass('active');
    })

    $('.closeBtn').click(function (e) {
        $('.searchBox').removeClass('active');
        $('.search').removeClass('active');
    });

    $('.menuToggle').on('click', () => {
        $('#navigation0').toggleClass('active');
        $('.searchBox').removeClass('active');
        $('.search').removeClass('active');
    })
}

window.onscroll = function () {
    if ((window.innerHeight + window.scrollY >= window.innerHeight + 50) && (window.innerHeight + window.scrollY < document.body.offsetHeight)) {
        // $('body').css('background', 'blue');
        $('.navigation').css({visibility: 'visible', opacity: 1});
    }
    else
        $('.navigation').css({visibility: 'hidden', opacity: 0});
    // if (window.innerHeight + window.scrollY >= document.body.offsetHeight)
    // {
    //     $('.navigation').css({visibility: 'hidden', opacity: 0});
    // }
    // else
    //     $('.navigation').css({visibility: 'visible', opacity: 1});
    
}

function nav(view) {
    $('.list').each(function (indexInArray, valueOfElement) {
        $('.list').eq(indexInArray).removeClass('active');
    });
    $(view).addClass('active');
}