function shuffle() {
    var cards = $(".shuffle-me");
    for (var i = 0; i < cards.length; i++) {
        var target = Math.floor(Math.random() * cards.length - 1) + 1;
        var target2 = Math.floor(Math.random() * cards.length - 1) + 1;
        cards.eq(target).before(cards.eq(target2));
    }
    console.log("shuffled");
};

var first = true;
function placeButtonsInForm() {
    var form = document.getElementById("myform");
    var b1 = document.getElementById("b1");
    var b2 = document.getElementById("b2");
    form.appendChild(b1);
    form.appendChild(b2);
    var element = document.getElementById("hint");
    element.classList.remove("d-none");
}
function showHint() {
    $('#modalHint').modal('show');
};
function showCorrect() {
    $('#modalCorrect').modal('show');
};
function showWrongOrHintIfFirst(id) {
    if (first) {
        first = false;
        showHint();
        var btn = document.getElementById("b" + id);
        btn.disabled = true;
        btn.setAttribute("class", "shuffle-me btn btn-sm btn-danger btn-block mt-1 mb-3")
    }
    else {
        $('#modalWrong').modal('show');
    }
};

document.addEventListener("DOMContentLoaded", function () {
    shuffle();
});