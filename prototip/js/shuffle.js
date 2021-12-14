function shuffle() {
    var cards = $(".questioncard");
    for (var i = 0; i < cards.length; i++) {
        var target = Math.floor(Math.random() * cards.length - 1) + 1;
        var target2 = Math.floor(Math.random() * cards.length - 1) + 1;
        cards.eq(target).before(cards.eq(target2));
    }
    console.log("shuffled");
};

var first = true;
function showHint() {
    $('#modalHint').modal('show');
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