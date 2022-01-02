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
}
function showHint() {
    $('#modalHint').modal('show');
    var element = document.getElementById("hint");
    element.classList.remove("d-none");
};
function showCorrect() {
    $('#modalCorrect').modal('show');
};
function showWrongOrHintIfFirst() {
    if (first) {
        first = false;
        showHint();
    }
    else {
        $('#modalWrong').modal('show');
    }
};

document.addEventListener("DOMContentLoaded", function () {
    shuffle();
});