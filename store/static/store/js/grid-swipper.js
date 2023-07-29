var swiper_grid = new Swiper(".categories-grid-swiper", {
	slidesPerView: 3,
	autoplay: {
		delay: 3000,
        disableOnInteraction: false,
	},
	breakpoints: {
		"@0.00": {
			slidesPerView: 1,
			spaceBetween: 15,
			grid: {
				rows: 2,
			},
	  },
	  "@0.75": {
		slidesPerView: 3,
		// spaceBetween: 20,
	  },
	},
	spaceBetween: 15,
	pagination: {
	el: ".swiper-pagination",
	clickable: true,
	renderBullet: function (index, className) {
		return '<span class="' + className + '">' + "</span>";
	  },
	},
});