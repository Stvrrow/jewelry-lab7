// Первая (громоздкая) реализация из методички: стили меняются у каждого элемента отдельно.
// В проекте подключена компактная версия fold-post.js; этот файл оставлен для сравнения.
var foldBtns = document.getElementsByClassName("fold-button");
for (var i = 0; i < foldBtns.length; i++) {
    foldBtns[i].addEventListener("click", function(e) {
        if (e.target.className == "fold-button folded") {
            e.target.innerHTML = "свернуть";
            e.target.className = "fold-button";
            var displayState = "block";
        } else {
            e.target.innerHTML = "развернуть";
            e.target.className = "fold-button folded";
            var displayState = "none";
        }
        var post = e.target.parentElement.parentElement;
        post.getElementsByClassName('article-author')[0].style.display = displayState;
        post.getElementsByClassName('article-created-date')[0].style.display = displayState;
        post.getElementsByClassName('jewelry-info')[0].style.display = displayState;
        post.getElementsByClassName('article-text')[0].style.display = displayState;
    });
}
