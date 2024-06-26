/* MATHJax */
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

/* ZOOM */
document.querySelectorAll('.zoom').forEach(item => {
    item.addEventListener('click', function () {
        this.classList.toggle('image-zoom');
    })
});
document.querySelectorAll('.zoom2').forEach(item => {
    item.addEventListener('click', function () {
        this.classList.toggle('image-zoom2');
    })
});