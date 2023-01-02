$(document).ready(function () {
// on document ready
// check for url in cache
// if there is no url, redirect to scratchpad.com/newpage
// if there is a url, redirect to scratchpad.com/<url>

if(localStorage.getItem('cached_url') === null) {
    window.location.replace("newpage");
} else {
    window.location.replace(localStorage.getItem('cached_url'));
}

});