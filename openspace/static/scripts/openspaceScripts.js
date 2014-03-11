// scatter fade
$(document).ready(function() {
    $(".jsFade").hide();
    $(".jsFade").each(function() {
       var speed = Math.floor((Math.random()*111)+1)
       $(this).fadeIn(speed*10); 
    });
});

// constant fade
$(document).ready(function() {
    $(".jsSteadyFade").hide();
    $(".jsSteadyFade").each(function() {
       $(this).fadeIn(999); 
    });
});

// activity fade
$(document).ready(function() {
    $(".latestAction").hide();
    $(".latestAction").each(function() {
       $(this).fadeIn(999); 
    });
});

// toggles hidden elements
$(document).ready(function() {
    $(".hiddenToggle").hide();
    $(".toggle").click(function(){
        var container = "#" + $(this).attr("data-mark");
        $(container).slideToggle(75, "linear");
    });
});

// add tags to profileTag input form
$(document).ready(function() {
    $(".profileTag").click(function(){
        var id = $(this).attr("data-id");
        var target = "#" + id + "_profile_new_tags";
        var $edit = $(target).find("input");
        var curValue = $edit.val();
        var newValue = "";
        if(curValue.length == 0){
            newValue = curValue + $(this).attr("data-tag");
        }
        else {
            if(curValue.substring(curValue.length - 2, curValue.length) != ", "){
                newValue = curValue + ", " + $(this).attr("data-tag");
            }
            else {newValue = curValue + $(this).attr("data-tag");}
        }
        $edit.val(newValue); 
    });
});

// add tags to postTag input form
$(document).ready(function() {
    $(".postTag").click(function(){
        var id = $(this).attr("data-flag");
        var target = "#" + id + "_post_new_tags";
        var $edit = $(target).find("input");
        var curValue = $edit.val();
        var newValue = "";
        if(curValue.length == 0){
            newValue = curValue + $(this).attr("data-tag");
        }
        else {
            if(curValue.substring(curValue.length - 2, curValue.length) != ", "){
                newValue = curValue + ", " + $(this).attr("data-tag");
            }
            else {newValue = curValue + $(this).attr("data-tag");}
        }
        $edit.val(newValue);
    });
});

// enter submit
$(function() {
    $('form').each(function() {
        $(this).find('input').keypress(function(e) {
            // Enter pressed?
            if(e.which == 10 || e.which == 13) {
                this.form.submit();
            }
        });
    });
});