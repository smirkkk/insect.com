function copyToClipboard(val) {
    var t = document.createElement("textarea");
    document.body.appendChild(t);
    t.value = val;
    t.select();
    document.execCommand('copy');
    document.body.removeChild(t);
}

function openNav() {
    $(".overlay").show();
    $("#mySidenav").toggleClass('expanded');
    // document.getElementById("mySidenav").style.width = "350px";
}

function openMobileNav() {
    $(".overlay").show();
    $("#mySidenav").toggleClass('expanded');

    // document.getElementById("mySidenav").style.width = "100%";
}

function closeNav() {
    $(".overlay").hide();
    $("#mySidenav").toggleClass('expanded');
}

jQuery(function($)
{
    $(document).ready(function () {

        var submenu = $(".menutitle").next("ul");
        submenu.slideUp();

        $(function(){
            $('#menu_button, #mobile_menu_button').click(function(e){
                e.stopPropagation();
                // $('.ui.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
            });
        });

        $(".menutitle").click(function(){
            var submenu = $(this).next("ul");

            if( submenu.is(":visible") ){
                tmp = $(this).text().replace(/\-/g,'+');
                $(this).text(tmp)
                submenu.slideUp();
            }else{
                tmp = $(this).text().replace(/\+/g,'-');
                $(this).text(tmp)
                submenu.slideDown();
            }
        });

        //사이드메뉴
        $('.submenutitle').each(function(idx)
        {
            var s = $(this),
            a = s.find('li>a');

            a.bind('focus mouseenter', function(e)
            {
                a.removeClass('active');
                $(this).addClass('active');
            });
        });

    });

});