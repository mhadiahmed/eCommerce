$(document).ready(function(){
	$(".mark-Down").each(function(){
		var content = $(this).text()
		var markDown = marked(content)
		$(this).html(markDown)
	});


	var ItemsTitle = $("#id_title");
	function setTitile(value){
		$("#title-pr").text(value)
	}
	setTitile(ItemsTitle.val())
	ItemsTitle.keyup(function(){
		var newContent = $(this).val()
		setTitile(newContent)
	});
// date
	var itemsDate = $("#id_date");
	function setDate(value){
		$("#date-pr").text(value)
	}
	setDate(itemsDate.val())
	itemsDate.keyup(function(){
		var newContent = $(this).val()
		setDate(newContent)
	});
// image
	var itemImage = $("#id_image");
	function setImage(value){
		$("#img-pr").text(value)
	}
	setImage(itemImage.val())
	itemImage.keyup(function(){
		var newContent = $(this).val()
		setImage(newContent)
	});

// price
	var itemsPrice = $("#id_price");
	function setPrice(value){
		$("#price-id").text(value)
	}
	setPrice(itemsPrice.val())
	itemsPrice.keyup(function(){
		var newContent = $(this).val()
		setPrice(newContent)
	});
// dis
	var itemsDis = $("#id_dis");
	function setDis(value){
		$("#dis-pr").text(value)
	}
	setDis(itemsDis.val())
	itemsDis.keyup(function(){
		var newContent = $(this).val()
		setDis(newContent)
	});

	$(".coment-r-btn").click(function(event){
		event.preventDefault();
		$(this).parent().next(".comment-Reply").toggle();

	});

// sing up page

	$('#login h2 span').click(function(){
		$(this).addClass('active').siblings().removeClass('active');
		$('#login form').hide();
		$('.' + $(this).data('class')).fadeIn(100);
	});

	// first name field

	$('#id_first_name').blur(function(){

		if ($(this).val().length <= 3){

			$(this).css('border', '1px solid #F00');
			firstname = true;
		} else {
			firstname = false;
			$(this).css('border', '1px solid #080');
		}
	});
	
	// last namefield

	$('#id_last_name').blur(function(){

		if ($(this).val().length <= 3){

			$(this).css('border', '1px solid #F00');
			lastname = true;
		} else {
			lastname = false;
			$(this).css('border', '1px solid #080');
		}
	});

	// user name field 

	$('#id_username').blur(function(){

		if ($(this).val().length <= 2){

			$(this).css('border', '1px solid #F00');
			username = true;
		} else {
			username = false;
			$(this).css('border', '1px solid #080');
		}
	});

	// email field 1

	$('#id_email').blur(function(){

		if ($(this).val() === ''){

			$(this).css('border', '1px solid #F00');
			email1 = true;
		} else {
			email1 = false;
			$(this).css('border', '1px solid #080');
		}
	});


	// email field 2

	$('#id_email2').blur(function(){

		if ($(this).val() != $('#id_email').val() && $(this).val() === '' ){

			$(this).css('border', '1px solid #F00');
			email2 = true;
		} else {
			email2 = false;
			$(this).css('border', '1px solid #080');
		}
	});





	// password field 1

	$('#id_password').blur(function(){

		if ($(this).val() === ''){

			$(this).css('border', '1px solid #F00');
			password = true;
		} else {
			password = false;
			$(this).css('border', '1px solid #080');
		}
	});


	// password field 2

	$('#id_password2').blur(function(){

		if ($(this).val() != $('#id_password').val()){

			$(this).css('border', '1px solid #F00');
			password2 = true;
		} else {
			password2 = false;
			$(this).css('border', '1px solid #080');
		}
	});

	// singup form 

	$('#mian-form').submit(function (e) {
		if (firstname === true || lastname === true || username === true || email1 === true || email2 === true || password === true || password2 === true){
			e.preventDefault();
		}
	});

	// password field
	$('#passlog').blur(function(){

		if ($(this).val() === ''){

			$(this).css('border', '1px solid #F00');
		
		} else {
		
			$(this).css('border', '1px solid #080');
		}
	});

	// user field
	$('#user').blur(function(){

		if ($(this).val().length <= 2){

			$(this).css('border', '1px solid #F00');
			username = true;
		} else {
			username = false;
			$(this).css('border', '1px solid #080');
		}
	});


// this is password change page =====================================

	// old password field 

	$('#id_old_password').blur(function(){

		if ($(this).val() === ''){

			$(this).css('border', '1px solid #F00');
			old_password = true;
		} else {
			old_password = false;
			$(this).css('border', '1px solid #080');
		}
	});

	// new password field 1

	$('#id_new_password1').blur(function(){

		if ($(this).val() === ''){

			$(this).css('border', '1px solid #F00');
			newpassword1 = true;
		} else {
			newpassword1 = false;
			$(this).css('border', '1px solid #080');
		}
	});


	// new password field 2

	$('#id_new_password2').blur(function(){

		if ($(this).val() != $('#id_new_password1').val()){

			$(this).css('border', '1px solid #F00');
			newpassword2 = true;
		} else {
			newpassword2 = false;
			$(this).css('border', '1px solid #080');
		}
	});

	// password reset form

	$('form').submit(function (e) {
		if (old_password === true || newpassword1 === true ||newpassword2 === true){
			e.preventDefault();
		}
	});


//  this is custmize page 

	//  phone field

	$('#id_phone').blur(function(){

		if ($(this).val().length < 10){

			$(this).css('border', '1px solid #F00');
			phone = true;
		} else {
			phone = false;
			$(this).css('border', '1px solid #080');
		}
	});

	// City field

	$('#id_city').blur(function(){

		if ($(this).val() === ''){

			$(this).css('border', '1px solid #F00');
			city = true;
		} else {
			city = false;
			$(this).css('border', '1px solid #080');
		}
	});

	
	// Company field

	$('#id_company').blur(function(){

		if ($(this).val() === ''){

			$(this).css('border', '1px solid #F00');
			company = true;
		} else {
			company = false;
			$(this).css('border', '1px solid #080');
		}
	});

	// custmize form
	
	$('form').submit(function (e) {
		if (phone === true || city === true || company === true){
			e.preventDefault();
		}
	});


	// $('body').css("overflow","auto")


});

	//jQuery for page scrolling feature - requires jQuery Easing plugin


$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});

//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $(document).on('click', 'a.page-scroll', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});




$(window).load(function() {
	
	var loading = $('.load-d .loader')
	// $('body').css("overflow","hidden")
    loading.fadeOut(1000,function(){
    	$(this).parent().fadeOut(1000,function(){
    		$(this).remove()
    		$('body').css("overflow","auto")
    	})
    })

})