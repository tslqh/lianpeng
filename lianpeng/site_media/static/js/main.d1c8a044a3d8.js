(function(){var c;$(".search").submit(function(){var j=$(this).find(".query").val();var i=$(this).attr("action")+j;if(c){c.navigate(i,{trigger:true})}else{window.location.href=i}return false});$("#feedback .confirm").click(function(){if($(this).hasClass("disabled")){return false}$(this).addClass("disabled");var j=$("#feedback textarea").val();var i={text:j};i=JSON.stringify(i);$.ajax({url:"/api/v1/feedback/",data:i,type:"POST",contentType:"application/json",dataType:"application/json"}).complete(function(){$("#feedback textarea").hide();$("#feedback .success").show()});return false});$("#feedback").on("hidden",function(){$("#feedback textarea").val("");$("#feedback .confirm").removeClass("disabled");$("#feedback textarea").show();$("#feedback .success").hide()});F={fetch_title:function(i,j){$.post("/harvest/pageinfo/",{url:i},j)},url_domain:function(j){var i=document.getElementById("url-template");i.href=j;var k=i.hostname;if(i.port&&i.port!=80){k+=":"+i.port}return k},form2json:function(j){var k={};var i=$(j).serializeArray();$.each(i,function(){if(k[this.name]!==undefined){if(!k[this.name].push){k[this.name]=[k[this.name]]}k[this.name].push(this.value||"")}else{k[this.name]=this.value||""}});return k},show_paginator:function(i,k,l){var j=i;if(j.collection.total_count>j.collection.paginationConfig.ipp){j.$(".paginator").pagination({total_pages:Math.ceil(j.collection.total_count/j.collection.paginationConfig.ipp),current_page:j.collection.currentPage,display_max:k,callback:function(m,n){l();j.collection.loadPage(n)}}).show()}else{j.$(".paginator").hide()}}};$.fn.spin=function(i){this.each(function(){var k=$(this),j=k.data();if(j.spinner){j.spinner.stop();delete j.spinner}if(i!==false){j.spinner=new Spinner($.extend({color:k.css("color")},i)).spin(this)}});return this};var a="/api/v1/user/"+USER_ID;var h=Backbone.Model.extend({urlRoot:"/api/v1/bookmark/"});var f=Backbone.Collection.extend({parse:function(i){this.total_count=i.meta.total_count;return i.objects}});var e=Backbone.Model.extend({urlRoot:"/api/v1/list/"});var d=e.extend({});var g=f.extend({model:e,initialize:function(){Backbone.Pagination.enable(this,{page_attr:"offset",ipp:100,ipp_attr:"limit"})},baseUrl:"/api/v1/list/"});var b=Backbone.View.extend({events:{"click .list-name":"redirect"},initialize:function(){var i=this;this.model.bind("change",this.change_name,this)},})}).call(this);