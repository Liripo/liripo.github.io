(function() {
  function center_el(tagName) {
    var tags = document.getElementsByTagName(tagName), i, tag;
    for (i = 0; i < tags.length; i++) {
      tag = tags[i];
      var parent = tag.parentElement;
      // center an image if it is the only element of its parent
      if (parent.childNodes.length === 1) {
        // if there is a link on image, check grandparent
        if (parent.nodeName === 'A') {
          parent = parent.parentElement;
          if (parent.childNodes.length != 1) continue;
          parent.firstChild.style.border = 'none';
        }
        if (parent.nodeName === 'P') parent.style.textAlign = 'center';
      }
    }
  }
  var tagNames = ['img', 'embed', 'object'];
  for (var i = 0; i < tagNames.length; i++) {
    center_el(tagNames[i]);
  }
})();
/*//文章 toc 跟随
var nav = $(".tocify");
nav.removeClass("hide");
var navTop = $(".post-content").offset().top;
var w = $(window).width()/2 + 400;
nav.css("left", w);
nav.css("top", navTop);
$(window).scroll(function() {
    var scrolls = $(this).scrollTop();
    if (scrolls > navTop) {
      nav.css({"top":0,"position":"fixed"});
    } else {
      nav.css({"top":navTop,"position":"absolute"});
    };
});*/
iterativeUL: function($dom) {
    var li_list = []
    $dom.children("li").each(function(i, item) {
        var _li = { 
            url: $(item).children("a").attr("href"), 
            name: $(item).children("a").text(),
            children: []
        }   
        $sub_ul = $(item).children("ul")
        if ($sub_ul.length > 0) {
            _li.children = main.iterativeUL($sub_ul)
        }   
        li_list.push(_li)
    })  
    return li_list
};
iterativeUI: function(root, template, prefix) {
    template += "<ul>"
    $.each(root, function(i, item) {
        var next_prefix = prefix + String(i+1) + "." 
        template += '<li>'+
                        '<i class="fa fa-hand-o-right" aria-hidden="true"></i>'+
                        '<span class="title-icon "></span>'+
                        '<a href="99991997"><b>99991998  </b>99991999</a>'
                           .replace("99991997", item.url)
                           .replace("99991999", item.name)
                           .replace("99991998", next_prefix) +
                    '</li>'
        if (item.children.length > 0) {
            template = main.iterativeUI(item.children, template, next_prefix)
        }   
    })  
    template += "</ul>"
    return template
};
initNavigations: function() {
    var $navigations = $("#TableOfContents");
    /* 这是个大坑, 需要大于号>来限制只选择一级子元素，否则会有多组ul被匹配到 */
    var root = main.iterativeUL($("#TableOfContents > ul"))
    if (root.length <= 0) {
        return;
    }

    var html = main.iterativeUI(root, '', '')

    //重新替换Toc模板
    $navigations.html(html)

    //由于导航栏固定,所以调整目录锚点往上偏移导航栏高度的距离
    var fixSet = $("#main-navbar").height() + 10; 
    $('nav#TableOfContents a[href^="#"][href!="#"]').click(function(e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: $(decodeURI(this.hash)).offset().top - fixSet}, 400);
    }); 
};