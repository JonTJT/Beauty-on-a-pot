$(document).ready(function() {
   /* 
    *	This function toggles the nav menu active/inactive status as 
    *	different pages are selected. It should be called from $(document).ready() 
    *	or whenever the page loads. 
    */ 
    function activateMenu() 
    { 
        var current_page_URL = location.href; 

        $(".navbar-nav a").each(function() 
        {
            var target_URL = $(this).prop("href"); 
            if (target_URL === current_page_URL)
            { 
                $('nav a').parents('li, ul').removeClass('active');
                $(this).parent('li').addClass('active');
                return false; 
            } 
        }); 
    } 

    function imgPopup(className,src){
        if(document.getElementsByClassName("img-popup")[0]== null){
            var popup = document.createElement("span");
            popup.setAttribute("class" , "img-popup");
            var animal = className.split(" ");
            popup.innerHTML = "<img src=images/" + animal[1] + "_large.jpg/>";
            document.getElementsByClassName(className)[0].before(popup);
            document.addEventListener("click", function(ev){
                ev.stopPropagation();   
                document.getElementsByClassName("img-popup")[0].remove();
            }, {once: true});
        } else{
            document.getElementsByClassName("img-popup")[0].remove();
        }
    }
    
    activateMenu();
    var imgThumbnails = document.getElementsByClassName("img-thumbnail")
    for(var i = 0; i < imgThumbnails.length; i++){
        let className = imgThumbnails[i].className;
        let src = imgThumbnails[i].src;
        imgThumbnails[i].addEventListener("click", function(ev){
            ev.stopPropagation();
            imgPopup(className,src);
        });
    }
});