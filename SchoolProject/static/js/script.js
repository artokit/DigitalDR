"use strict";
const domen = 'http://127.0.0.1:8000/';
const GET_MENU_URL = domen + 'get_menu';
const ADD_NEW_USER_URL = domen + 'add_user';
const F_URL = domen + 'f';
const LOGIN_URL = domen + 'login';

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
    close.onclick = () => {
        document.getElementsByClassName('back')[0].remove();
    };
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
    xhr.open('GET', GET_MENU_URL);
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
    elem_load.style.top = window.pageYOffset + 'px';
    document.body.style.overflowY = 'hidden';
    func();
}

function del_load() {
    let elem_load = document.getElementById('load');
    elem_load.remove();
}

function anim_error(elem) {
    elem.style.animation = 'error_elem_anim .8s ease';
    setTimeout(() => {
        elem.style.animation = 'none';
    }, 1000);
}

function add_new_user() {
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0];
    let first_name = document.getElementById('id_first_name');
    let last_name = document.getElementById('id_last_name');
    let email = document.getElementById('id_email');
    let username = document.getElementById('id_username');
    let password1 = document.getElementById('id_password1');
    let password2 = document.getElementById('id_password2');
    let error_messages = document.getElementsByClassName('error_messages')[0];
    let user_class = document.getElementById('id_select_class');

    if (password1.value !== password2.value) {
        error_messages.innerText = 'Пароли не совпадают.';
        anim_error(password1);
        anim_error(password2);
        return false;
    }

    if (!user_class.value) {
        error_messages.innerText = 'Выберите класс.';
        user_class.style.animation = 'error_elem_anim_from_black 1s ease';
        setTimeout(() => {
            user_class.style.animation = 'none';
        }, 1000);
        return false;
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', ADD_NEW_USER_URL);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.onload = function () {
        let res = JSON.parse(xhr.response);

        if (!res.success) {
            error_messages.innerText = res.message;
            let elem_error = document.getElementById(res.elem_error_id);
            anim_error(elem_error);
            return false;
        } else if (res.success) {
            document.location.href = F_URL;
        }
    };

    xhr.send(`csrfmiddlewaretoken=${csrf.value}&first_name=${first_name.value}&last_name=${last_name.value}&email=${email.value}&username=${username.value}&password=${password1.value}&user_class=${user_class.value}`);
}

function replaceBlock(elem) {
    let student = document.getElementById('student');
    let teacher = document.getElementById('teacher');
    let login__sform = document.getElementsByClassName('login__sform')[0];
    let login__tform = document.getElementsByClassName('login__tform')[0];
    if (elem.id === 'teacher') {
        teacher.className = 'active';
        student.className = '';
        login__sform.style.opacity = '0';
        login__sform.style.visibility = 'hidden';
        login__tform.style.opacity = '1';
        login__tform.style.visibility = 'visible';
    }
    else {
        teacher.className = '';
        student.className = 'active';
        login__sform.style.opacity = '1';
        login__sform.style.visibility = 'visible';
        login__tform.style.opacity = '0';
        login__tform.style.visibility = 'hidden';
    }
}

function ModalLogin() {
    document.documentElement.style.overflowY = 'hidden';
    document.getElementsByClassName('wrap')[0].scrollIntoView({
        block: 'start'
    });
    let modalWindow = document.getElementsByClassName('wrap_login')[0];
    let elem_close = document.getElementsByClassName('close')[0];
    elem_close.onclick = () => {
        modalWindow.style.display = 'none';
        document.documentElement.style.overflowY = 'scroll';
    };
    if (modalWindow.classList.length === 2) {
        return false;
    }
    else {
        modalWindow.style.display = 'block';
    }
}

function login() {
    let elem_active = document.getElementsByClassName('active')[0];
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0];
    const xhr = new XMLHttpRequest();
    xhr.onload = () => {
        let res = JSON.parse(xhr.response);
        if (res['success']) {
            window.location = domen + 'main';
        }
    };
    console.log(csrf.value);
    if (elem_active.innerText === 'Учитель') {
        let code__input = document.getElementsByClassName('code__input')[0];
        xhr.open('POST', LOGIN_URL);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send(`csrfmiddlewaretoken=${csrf.value}&mode=teacher&code=${code__input.value}`);
    }
}

function viewNav() {
    let nav = document.getElementsByClassName('nav')[0];
    nav.style.transition = '.3s';
    nav.style.left = '0'
}

function closeNav() {
    let nav = document.getElementsByClassName('nav')[0];
    nav.style.transition = '.3s';
    nav.style.left = '-200vw';
}