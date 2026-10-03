// Компактная реализация: класс folded ставится на весь пост (.one-post),
// а что именно скрывать, описано в CSS.
var foldBtns = document.getElementsByClassName("fold-button");
for (var i = 0; i < foldBtns.length; i++) {
    foldBtns[i].addEventListener("click", function(e) {
        var post = e.target.closest(".one-post");
        var folded = post.classList.toggle("folded");
        e.target.innerHTML = folded ? "развернуть" : "свернуть";
    });
}
