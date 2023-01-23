window.onscroll = function () {
    if (window.innerHeight + window.scrollY >= window.innerHeight + 50) {
        // $('body').css('background', 'blue');
        $('.navigation').css({visibility: 'visible', opacity: 1});
    }
    else {
        $('.navigation').css({visibility: 'hidden', opacity: 0});
    }
}

window.onload = function () {
    $('#home').on('click', () => {
        nav('#home');
    })
    $('#user').on('click', () => {
        nav('#user');
    })
    $('#chat').on('click', () => {
        nav('#chat');
    })
    $('#settings').on('click', () => {
        nav('#settings');
    })
    $('#picture').on('click', () => {
        nav('#picture');
    })
    $('#login').on('click', () => {
        nav('#login');
    })
    $('#logout').on('click', () => {
        nav('#logout');
    })
    $('#search').on('click', () => {
        nav('#search');
    })

    if (window.innerWidth > 750)
    {
        $('#carouselExampleIndicators').height(window.innerHeight - 40);
        $('.d-block').height(window.innerHeight - 40);
        console.log();
    }

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

function nav(view) {
    $('.list').each(function (indexInArray, valueOfElement) {
        $('.list').eq(indexInArray).removeClass('active');
    });
    $(view).addClass('active');
}