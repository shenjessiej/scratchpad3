var intro =
    ['<style>',
        '  body {background: #88a36f;}',
        '  .container {',
        '    background: #fff;',
        '    padding: 50px;',
        '    margin: 50px auto;',
        '    width: 400px;',
        '    font-family: sans-serif;',
        '    border-radius: 10px;',
        '  }',
        '</style>',
        '<div class="container">',
        '    <h1>scratchpad 3</h1>  ',
        '  <p>Hello! This is a simple web-based live-reload HTML/CSS/JS text editor! You can do code-y things here like in old Scratchpad. </p>',
        ' <p>  DM <b>tom nook apologist#7578</b> on discord if you encounter any bugs!   ',
        ' <p>  Rest in pieces Scratchpad (??-2020). ',
        '</div>'].join('\n');




$(document).ready(function () {


    //console.log("page loaded");
    // Save the current url to the cache.
    localStorage.setItem('cached_url', window.location.pathname.replace(/\//,''));

    // Scratchpad Intro
    //--------------------------------------------------------------------------------

    // Set up iframe.
    var iframe = document.getElementById('preview'),
        iframedoc = iframe.contentDocument || iframe.contentWindow.document;
    iframedoc.body.setAttribute('tabindex', 0);


    iframedoc.body.innerHTML = editor.getValue();
    editor.clearSelection();

    // when editor is updated
    editor.getSession().on('change', function (e) {
        console.log("trying to save data");
        iframedoc.body.innerHTML = editor.getValue();

        // send ajax post request to database saving current editor content to ddb

        var currenttitle = document.title;
            
        $.ajax({
            type: "POST",
            url: '/save_content',
            data: {
                "url_identifier": window.location.pathname.replace(/\//,''),
                "code_content": editor.getValue(),
                "page_title": currenttitle
            },
            dataType: 'json',
            success: function(data){
                console.log("Successfully saved!");
                console.log(data);
            }
        });
    
        // Resize the menu icon if appropriate
        var linesOfCode = editor.session.getLength();
        if (linesOfCode < 10) {
            $('#menu').attr('class', 'small')
        } else if (linesOfCode > 9 && linesOfCode < 99) {
            $('#menu').attr('class', 'medium')
        } else if (linesOfCode > 99 && linesOfCode < 999) {
            $('#menu').attr('class', 'large')
        } else if (linesOfCode > 999) {
            $('#menu').attr('class', 'x-large')
        }
    });

    var editorwidth = $('#editor').width() + 2;
    $('#preview').css('left', editorwidth);


});

// Ace Editor setup

var editor = ace.edit("editor");
editor.setTheme("ace/theme/tomorrow_night_eighties");
editor.setHighlightActiveLine(false);
editor.getSession().setTabSize(2);
document.getElementById('editor').style.fontSize = '11px';
editor.commands.removeCommand('gotoline');
editor.setShowPrintMargin(false);
editor.getSession().setMode("ace/mode/html");
editor.commands.addCommand({
    name: 'showHelp',
    bindKey: {win: 'Ctrl-/', mac: 'Command-/'},
    exec: function (editor) {
        $('#help').toggleClass('visible');
    }
});
editor.commands.addCommand({
    name: 'toggleFullscreen',
    bindKey: {win: 'Ctrl-i', mac: 'Command-i'},
    exec: function (editor) {
        toggleFullscreen();
    }
});

// dragbar

var dragging = false;
var wpoffset = 0;
$('#editor-dragbar').mousedown(function (e) {
    e.preventDefault();
    window.dragging = true;

    var editor = $('#editor');
    var right_offset = editor.offset().right + wpoffset;

    // Set editor opacity to 0 to make transparent so our wrapper div shows
    editor.css('opacity', 0);

    // handle mouse movement
    $(document).mousemove(function (e) {

        var actualX = e.pageX + wpoffset;
        // editor width
        var ewidth = actualX + right_offset;
        var dragbarWidth = $('#editor-dragbar').width();

        var prevwidth = $(window).width() - e.pageX - dragbarWidth;
        var prevLeft = e.pageX + dragbarWidth;

        // Set wrapper width
        $('#editor').css('width', e.pageX);
        $('#navbar').css('width', e.pageX);

        $('#preview').css('width', prevwidth);
        $('#preview').css('left', prevLeft);

        // Move dragbar
        $('#editor-dragbar').css('opacity', 0.15).css('left', e.pageX);


    });

});

$('#editor-dragbar').mouseup(function (e) {

    if (window.dragging) {
        var editor = $('#editor');

        var actualX = e.pageX + wpoffset;
        var right_offset = editor.offset().right + wpoffset;
        var ewidth = actualX + right_offset;

        $(document).unbind('mousemove');

        // Set dragbar opacity back to 1
        $('#editor-dragbar').css('opacity', 1);

        // Set width on actual editor element, and opacity back to 1
        editor.css('width', e.pageX).css('opacity', 1);
        $('#preview').css('width', prevwidth);
        $('#preview').css('left', e.pageX);

        // Trigger ace editor resize()
        editor.resize();
        window.dragging = false;
    }

});

// resize preview frame when window is dragged
window.addEventListener("resize", function(){
    var editorWidth = $('#editor').width();
    var windowWidth = $(window).width();
    var dragbarWidth = $('#editor-dragbar').width();

    $('#preview').css('width', windowWidth - editorWidth - dragbarWidth);
    $('#preview').css('left', editorWidth + dragbarWidth);

});

// editing title stuff

$(document).on('click', '#title', function() {

    var element = $(this);
    var inputbox = $('<input id="titleinput"/>').val(element.text());

    $('#titleinput').css('width', $('#editor').width());

    element.replaceWith(inputbox);

    var save = function() {
        var p = $('<div id="title"/>').text(inputbox.val());
        inputbox.replaceWith(p);
        document.title = inputbox.val();
        $.ajax({
            type: "POST",
            url: '/save_content',
            data: {
                "url_identifier": window.location.pathname.replace(/\//,''),
                "code_content": editor.getValue(),
                "page_title": inputbox.val()
            },
            dataType: 'json',
            success: function(data){
                //console.log("Successfully title!");
                //console.log(data);
            }
        });    
    };

    inputbox.on('blur', save).focus();



});

// new page button
$(document).on('click', '#newpage', function() {

    var newpage = window.open("newpage", "_blank");
    newpage.focus();

    //var content = localStorage.getItem('editorKey') ? localStorage.getItem('editorKey') : intro;
    //var title = localStorage.getItem('titleKey') ? localStorage.getItem('titleKey') : intro;

    //uriContent = "data:application/octet-stream," + encodeURIComponent(content);
    //newWindow = window.open(uriContent, title + '.html');

});
