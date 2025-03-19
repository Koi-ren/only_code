var btn = document.getElementById('btn');

function leftClick() {
    btn.style.left = '0';
    fetch('/off')
        .then(response => response.text())
        .then(text => console.log(text));
}

function rightClick() {
    btn.style.left = '110px';
    fetch('/on')
        .then(response => response.text())
        .then(text => console.log(text));
}
