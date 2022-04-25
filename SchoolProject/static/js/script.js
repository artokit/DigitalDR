"use strict";
const domen = 'http://127.0.0.1:8000/';
const GET_MENU_URL = domen + 'get_menu';
const SETTINGS_URL = domen + 'settings';
const LOGIN_URL = domen + 'login';
const REQUESTS_STUDENTS_URL = domen + 'RequestsStudentsPost/';
const CHANGE_FOOD_URL = domen + 'change/foodMenu';
const CHANGE_INFORMATION_URL = domen + 'change/information/';
const GET_BALANCE = domen + 'balance/';
const ORDER_URL = domen + 'orders/'

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

    if (body) {
        modalBody.innerHTML = body;
    }

    let modalClose = document.createElement('div');
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
    modalClose.className = 'modal_close';
    html.appendChild(background);
    modalClose.appendChild(close);
    background.appendChild(modalWindow);
    modalWindow.appendChild(modalClose);
    modalWindow.appendChild(modalHead);
    modalWindow.appendChild(modalBody);
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
    func();
}

function del_load() {
    let elem_load = document.getElementById('load');
    elem_load.remove();
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

function login() {
    let elem_active = document.getElementsByClassName('active')[0];
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0];
    const xhr = new XMLHttpRequest();

    xhr.onload = () => {
        let res = JSON.parse(xhr.response);
        if (res['success']) {
            window.location = domen + 'main';
        }
        else {
            let active = document.getElementsByClassName('active')[0].innerText;
            let loginMessage = (active === 'Учитель')?document.getElementsByClassName('loginMessage')[1] : document.getElementsByClassName('loginMessage')[0];
            loginMessage.innerText = res['message'];
            loginMessage.style.transition = '.6s';
            loginMessage.style.backgroundColor = '#ff5454';
        }
    };

    if (elem_active.innerText === 'Учитель') {
        let code__input = document.getElementsByClassName('code__input')[0];
        xhr.open('POST', LOGIN_URL);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send(`csrfmiddlewaretoken=${csrf.value}&mode=teacher&code=${code__input.value}`);
    }

    else {
        let login = document.getElementById('username__input').value;
        let password = document.getElementById('password__input').value;
        xhr.open('POST', LOGIN_URL);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send(`csrfmiddlewaretoken=${csrf.value}&mode=student&password=${password}&login=${login}`);
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

function clickFoodBtn(elem) {
    if (elem.className.endsWith('active')) {
        elem.className = elem.className.slice(0, -7);
    }
    else {
        elem.className = elem.className + '_active';
    }
}

function saveStudentChoose() {
    let dinnerDays_active = document.getElementsByClassName('dinnerDay_active');
    let lunchDays_active = document.getElementsByClassName('lunchDay_active');
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0];
    const xhr = new XMLHttpRequest();

    let msg_elem = document.getElementsByClassName('success_message')[0];
    msg_elem.innerHTML = '';
    msg_elem.style.visibility = 'hidden';
    msg_elem.style.display = 'none';

    xhr.onload = () => {
        let res = JSON.parse(xhr.response);
        if (res['success'] === true) {
            msg_elem.innerHTML = 'Данные успешно сохранены';
            msg_elem.style.display = 'block';
            msg_elem.style.visibility = 'visible';
            msg_elem.style.transition = '.6s';
        }
    };

    xhr.open('POST', CHANGE_FOOD_URL);
    let obj_to_send = {
        dinner: {
            'Пн': false,
            'Вт': false,
            'Ср': false,
            'Чт': false,
            'Пт': false,
        },
        lunch: {
            'Пн': false,
            'Вт': false,
            'Ср': false,
            'Чт': false,
            'Пт': false,
        },
    }

    for (let key of dinnerDays_active) {
        obj_to_send.dinner[key.innerText] = true;
    }

    for (let key of lunchDays_active) {
        obj_to_send.lunch[key.innerText] = true;
    }

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(`csrfmiddlewaretoken=${csrf.value}&data=${JSON.stringify(obj_to_send)}`);
}

function studentAccept(elem, student_id) {
    let accept = (elem.className === 'buttonStudent buttonStudentAccept') ? 'accept':'cancel';
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0];
    const xhr = new XMLHttpRequest();

    xhr.onload = () => {
        let res = JSON.parse(xhr.response);
        if (res['success']) {
            let student_elem = document.getElementById('student' + String(student_id));
            student_elem.remove();
        }
    }

    xhr.open('POST', REQUESTS_STUDENTS_URL);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(`csrfmiddlewaretoken=${csrf.value}&id=${student_id}&type=${accept}`);
}

function saveInformation() {
    const xhr = new XMLHttpRequest();
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0];
    let first_name = document.getElementById('id_first_name').value;
    let last_name = document.getElementById('id_last_name').value;
    let user_class = document.getElementById('selectClass__select').value;

    xhr.onload = () => {
        let res = JSON.parse(xhr.response);
        if (res['success']) {
            window.location.href = SETTINGS_URL;
        }
    }

    xhr.open('POST', CHANGE_INFORMATION_URL);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(`csrfmiddlewaretoken=${csrf.value}&first_name=${first_name}&last_name=${last_name}&user_class=${user_class}`);
}

function getBalance() {
    const xhr = new XMLHttpRequest();
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let card_num = document.getElementById('NumberCard').value;
    let hotMealBalance = document.getElementById('hotMealBalance');
    let CardId = document.getElementById('CardId');
    let time__lastTime = document.getElementsByClassName('time__lastTime')[0];
    let error = document.getElementsByClassName('BalanceError')[0];

    let d = new Date();
    let time = d.getTime();

    error.style.visibility = 'hidden';
    error.style.display = 'none';

    if ((Number(time__lastTime.innerHTML) + 180) * 1000 > time) {
        error.innerHTML = 'Отправьте запрос позже';
        error.style.visibility = 'visible';
        error.style.display = 'block';
        error.style.color = 'red';
        return false;
    }

    xhr.open('POST', GET_BALANCE, true);
    xhr.onload = () => {
        let res = JSON.parse(xhr.response);

        if (res['success']) {
            if (!hotMealBalance) {
                window.location.href = '';
            }

            hotMealBalance.innerText = res['result']['hot_meal_money'] + ' Р.';
            CardId.innerText = card_num;
        }

        else {
            error.innerHTML = res['text'];
            error.style.color = 'red';
            error.style.visibility = 'visible';
            error.style.display = 'block';
        }
    }

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(`csrfmiddlewaretoken=${csrf}&card_num=${card_num}`);
}

function kickUser(elem, user_id) {
    const xhr = new XMLHttpRequest();
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xhr.open('POST', ORDER_URL);

    xhr.onload = () => {
        let res = JSON.parse(xhr.response);

        if (res['success']) {
            elem.parentElement.parentElement.parentElement.remove();
        }
    }

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(`csrfmiddlewaretoken=${csrf}&user_id=${user_id}&act=kick`);
}

function showMoreInfo(elem) {
    const xhr = new XMLHttpRequest();
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xhr.open('POST', ORDER_URL);

    xhr.onload = () => {
        let res = JSON.parse(xhr.response);

        if (res['success']) {
            let cardNum = document.getElementById('cardNum');
            cardNum.innerText = res['card_num'];
            let cardBalance = document.getElementById('cardBalance');
            cardBalance.innerText = res['balance_card'] + ' Р';
            let lunch_elem = getHTMLFood('Завтраки', res['lunch']);
            let dinner_elem = getHTMLFood('Обеды', res['dinner']);
            let StudentChoose = document.getElementsByClassName('StudentChoose')[0];
            StudentChoose.innerHTML = lunch_elem + dinner_elem;
        }
    }

    let body = `<div class='userInfo'>
        <div class='userInfo__food checkFood'>
        <hr class='medium_hr'>
        <div class='checkFood__header'>Завтраки и обеды</div>
        <div class='StudentChoose'></div>
        </div>
        <div class='userInfo__cardInfo cardInfo'>
        <div class='cardInfo__header'>Информация о карте</div>
        <div class='cardInfo__cardNum'>Номер карты: <span id='cardNum'>Загрузка...</span></div>
        <div class='cardInfo__cardBalance'>Баланс: <span id='cardBalance'>Загрузка...</span></div>
        </div>
        </div>`;

    let userBlock = elem.parentElement.parentElement.parentElement;
    let fullName = userBlock.getElementsByClassName('userOrder__name')[0].textContent;
    let extraDataBlock = userBlock.getElementsByClassName('extraData')[0];
    let user_id = Number(extraDataBlock.getElementsByClassName('extraData__userID')[0].textContent);

    viewModalWindow(fullName, body);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(`csrfmiddlewaretoken=${csrf}&user_id=${user_id}&act=info`);
}

function getHTMLFood(head, data) {
    let table = '';
    for (let key in data) {
        if (data[key]) {
            table += `<div class="lunchDay_active">${key}</div>`;
        }
        else {
            table += `<div class="lunchDay"">${key}</div>`;
        }
    }

    let body = `<div class="lunchBlock foodBlock">
        <div class="lunch__header">
            ${head}
        </div>
        <div class="lunchDays">
            ${table}
        </div>
    </div>`;

    return body;
}

function hideMenuInfo(elem) {
    let menu_block = elem.parentElement.parentElement;
    let image = menu_block.getElementsByClassName('section_body__image')[0];
    let text = menu_block.getElementsByClassName('section_body__text')[0];
    let menu = menu_block.getElementsByClassName('section_body__menu')[0];

    if (!menu.style.height) {
        elem.innerHTML = 'Скрыть';
        menu.style.transition = '.3s';
        menu.style.height = '100%';
        menu.style.opacity = '1';

        text.style.transition = '.3s';
        text.style.opacity = '0';

        image.style.transition = '.3s';
        image.style.width = '0';
        image.style.opacity = '0';
    }
    else {
        elem.innerHTML = 'Посмотреть';
        menu.style.transition = '.3s';
        menu.style.height = '';
        menu.style.opacity = '0';

        text.style.transition = '.3s';
        text.style.opacity = '1';

        image.style.transition = '.3s';
        image.style.width = '100%';
        image.style.opacity = '1';
    }
}