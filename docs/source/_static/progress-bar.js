window.addEventListener("DOMContentLoaded", function() {
    var bar = document.getElementById("progress-bar");
    function updateBar() {
        var scrollTop = window.scrollY || document.documentElement.scrollTop;
        var docHeight = document.documentElement.scrollHeight - window.innerHeight;
        var percent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        bar.style.width = percent + "%";
    }
    window.addEventListener("scroll", updateBar);
    window.addEventListener("resize", updateBar);
    updateBar();
});