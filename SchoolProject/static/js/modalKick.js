"use strict";


function showKickedModalWindow() {
    let html = document.getElementsByTagName('html')[0];

    let background = document.createElement('div');
    background.className = 'back';

    let modalWindow = document.createElement('div');
    modalWindow.className = 'kickModalWindow';

    let modalHead = document.createElement('div');
    modalHead.className = 'modalHead'
    modalHead.innerText = 'Что-то пошло не так';

    let modalBody = document.createElement('div');
    modalBody.className = 'kickModalWindow__body';

    let modalBody__image = document.createElement('div');
    modalBody__image.innerHTML = `<img src="/static/images/trash.png">`
    modalBody__image.className = 'modalBody__image';

    let modalBody__text = document.createElement('div');
    modalBody__text.innerHTML = '<span>Учитель не принял твою заявку или выгнал тебя из класса. Возможно, ему не понравился твой профиль. Перейди по ссылке ниже, смени свои данные и заявка отправится снова.</span>' +
        '<div><a href="/settings">Настройки</a></div>';
    modalBody__text.className = 'modalBody__text';

    html.appendChild(background);
    background.appendChild(modalWindow);
    modalWindow.appendChild(modalHead);
    modalWindow.appendChild(modalBody);
    modalBody.appendChild(modalBody__image);
    modalBody.appendChild(modalBody__text);
}

showKickedModalWindow();
