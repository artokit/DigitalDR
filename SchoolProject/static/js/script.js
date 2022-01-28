"use strict";
function f() {
    let road = document.getElementById('road');
    let food = document.createElement('img');
    food.className = 'food';
    food.src = '../../../static/images/food/' + String(Math.floor(Math.random() * 10)) + '.png';
    road.appendChild(food);
    food.style.animation = 'show linear 8s';
    setTimeout(() => {food.remove()}, 7800)
}

function animateRoad() {
    let top_road = document.getElementsByClassName('top')[0]
    if (top_road.style.backgroundPosition === '17.5px center') {
        top_road.style.backgroundPosition = '0';
    }
    else {
        top_road.style.backgroundPosition = '17.5px';
    }
}


function closeModalWindow() {
    let background = document.getElementsByClassName('back')[0];
    background.remove();
}

function viewModalWindow(head, body) {
    if (document.getElementsByClassName('modal_window').length) {
        return false;
    }
    let background = document.createElement('div');
    let modalWindow = document.createElement('div');
    let modalHead = document.createElement('div');
    let modalBody = document.createElement('div');
    let close = document.createElement('div');
    let html = document.getElementsByTagName('html')[0];
    modalHead.innerHTML = `<h2>${head}</h2>`;
    close.onclick = closeModalWindow;
    close.className = 'close';
    modalHead.className = 'modal_head';
    modalBody.className = 'modal_body';
    background.className = 'back';
    modalWindow.className = 'modal_window';
    html.appendChild(background);
    background.appendChild(close);
    background.appendChild(modalWindow);
    modalWindow.appendChild(modalHead);
    modalWindow.appendChild(modalBody);
}

function viewRegForm() {
    let regForm = document.getElementsByClassName('registration')[0];
    regForm.style.visibility = 'visible';
    regForm.style.display = 'block';
    setTimeout(scrollToRegForm, 100);
}

function scrollToRegForm() {
    document.getElementsByClassName('form_reg__footer')[0].scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    })
}

function get_menu() {
    viewModalWindow('Меню', '');
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://artokit1.pythonanywhere.com/get_menu');
    xhr.onload = () => {
        let modalBody = document.getElementsByClassName('modal_body')[0];
        let res = JSON.parse(xhr.response);
        for (let i = 0; i < res.length; i++) {
            let row = document.createElement('div');
            let name = document.createElement('div');
            let cost = document.createElement('div');
            row.className = 'row';
            name.className = 'menu_name';
            cost.className = 'menu_cost';
            modalBody.appendChild(row);
            name.innerHTML = res[i].fields.name;
            cost.innerHTML = res[i].fields.cost + ' руб.';
            row.appendChild(name);
            row.appendChild(cost);
        }
        setTimeout(del_load, 1000)
    }
    xhr.send();
}

function load(func, content) {
    let elem_load = document.createElement('div');
    elem_load.id = 'load';
    let html = document.getElementsByTagName('html')[0];
    html.appendChild(elem_load);
    func();
}

function del_load() {
    let elem_load = document.getElementById('load');
    elem_load.remove();
}
