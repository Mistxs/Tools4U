
function displayErrorMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-success').addClass('alert-danger').slideDown();
    setTimeout(function() {
        errorMessage.slideUp();
    }, 3000);
}

function displaySuccessMessage(message) {
    var errorMessage = $('#error-message');
    errorMessage.text(message);
    errorMessage.removeClass('alert-danger').addClass('alert-success').slideDown();
    setTimeout(function() {
        errorMessage.slideUp();
    }, 3000);
}


function getClients() {
    var salon_id = document.getElementById('salon').value;
    var login = document.getElementById('login').value;
    var password = document.getElementById('pass').value;
    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

     return fetch('/getClients', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'salon_id': salon_id,
            'login': login,
            'password': password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var clients = data.text
            resultContainer.innerHTML = "";
            displayClients(clients)
            document.querySelectorAll('.btn').forEach(function(btn) {
                btn.disabled = false;
                btn.style.cursor = "pointer";
              });
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);

        }
    })
}

function displayClients(clients) {
    var table = $('<table class="table table-striped programs table-responsive">');
    var thead = $('<thead>').append('<tr><th>ID</th><th>Телефон</th><th>Имя</th><th>Отчество</th><th>Фамилия</th></tr>');
    table.append(thead);

    var tbody = $('<tbody>');
    for (var i = 0; i < clients.length; i++) {
        var record = clients[i];
        var row = $('<tr>');
        row.append('<td>' + record.id + '</td>');

        row.append('<td>' + record.phone + '</td>');
        row.append('<td>' + record.name + '</td>');
        row.append('<td>' + record.patronymic + '</td>');
        row.append('<td>' + record.surname + '</td>');

        tbody.append(row);
    }

    table.append(tbody);

    $('#result').empty().append(table);
}


function parseFIO() {
    var salon_id = document.getElementById('salon').value;
    var login = document.getElementById('login').value;
    var password = document.getElementById('pass').value;
    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

      return fetch('/parsefio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'salon_id': salon_id,
            'login': login,
            'password': password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var clients = data.text
            resultContainer.innerHTML = "";
            displayClients(clients)
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);

        }
    })
}


function getError() {
    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

      return fetch('/getError', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var clients = data.text
            resultContainer.innerHTML = "";
            displayClients(clients)
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);

        }
    })
}




function saveResult() {
    var salon_id = document.getElementById('salon').value;
    var login = document.getElementById('login').value;
    var password = document.getElementById('pass').value;
    var resultContainer = document.getElementById('result');

    // Показываем индикатор загрузки
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

      return fetch('/saveClients', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'salon_id': salon_id,
            'login': login,
            'password': password
        })
    })

    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            var clients = data.text
            resultContainer.innerHTML = "";
            displayClients(clients)
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);

        }
    })
}


function getReport() {
    var resultContainer = document.getElementById('result');
    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/getReport', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.blob())
    .then(blob => {
        // Создаем объект URL для файла
        var url = URL.createObjectURL(blob);

        // Меняем расширение файла на xlsx
        var a = document.createElement('a');
        a.href = url;
        a.download = 'report.xlsx';
        a.click();

        // Очищаем контейнер с результатом
        resultContainer.innerHTML = "";
    })
    .catch(error => {
        // Выводим сообщение об ошибке, если что-то пошло не так
        displayErrorMessage('Произошла ошибка при получении файла.');
    });
}


// блокируем все кнопки пока не получат данные
document.querySelectorAll('.btn').forEach(function(btn) {
  if (btn.innerText !== "Получить данные") {
    btn.disabled = true;
    btn.style.cursor = "not-allowed";
  }
});

