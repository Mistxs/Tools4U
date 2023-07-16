$(document).ready(function() {


$('#add-form').submit(function(e) {
        e.preventDefault();
        var salonId = $('#salon_id').val();
        if (salonId.trim() !== '') {
            addSalon(salonId);
            $('#salon_id').val('');
        }
    });
    loadSalons();
});

function addSalon(salonId) {
    var tagContainer = $('#tags-container');
    var existingSalons = tagContainer.find('.tag');
    for (var i = 0; i < existingSalons.length; i++) {
        var existingSalonId = $(existingSalons[i]).text().trim().split(' ')[0];
        if (existingSalonId === salonId) {
            displayErrorMessage('Салон уже существует в списке.');
            return;
        }
    }

    var tag = $('<div class="tag"></div>').text(salonId + ' ').append('<span onclick="removeSalon(this)">&#10006;</span>');
    tagContainer.append(tag);
    saveSalon(salonId);
}

function removeSalon(element) {
    var salonId = $(element).parent().text().trim().split(' ')[0]; // Извлекаем только ID салона
    $(element).parent().remove();
    deleteSalon(salonId);
}

function saveSalon(salonId) {
    $.ajax({
        url: '/save_salon',
        method: 'POST',
        data: {salon_id: salonId},
        success: function(response) {
            console.log('Salon saved successfully.');
            loadSalons(); // Загрузка обновленного списка салонов после сохранения
        }
    });
}

function deleteSalon(salonId) {
    $.ajax({
        url: '/delete_salon',
        method: 'POST',
        data: {salon_id: salonId},
        success: function(response) {
            console.log('Salon deleted successfully.');
            loadSalons(); // Загрузка обновленного списка салонов после удаления
        }
    });
}

function loadSalons() {
            $.ajax({
                url: '/get_salons',
                method: 'GET',
                success: function(response) {
                    var salons = response.salons;
                    var tagContainer = $('#tags-container');
                    tagContainer.empty(); // Очистка контейнера перед загрузкой нового списка салонов
                    for (var i = 0; i < salons.length; i++) {
                        var salonId = salons[i];
                        var tag = $('<div class="tag"></div>').text(salonId + ' ').append('<span onclick="removeSalon(this)">&#10006;</span>');
                        tagContainer.append(tag);
                    }
                }
            });
        }


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

var lastTimestamp = '';
var requestFlag = true;
function getLogs() {
        if (!requestFlag) {
            return;
        }

        requestFlag = false;

        $.getJSON('/logs', function(data) {
            var newLogs = data.filter(function(log) {
                return log.timestamp > lastTimestamp;
            });

            if (newLogs.length > 0) {
                for (var i = 0; i < newLogs.length; i++) {
                    var log = newLogs[i];
                    var timestamp = log.timestamp;
                    var message = log.message;

                    var logItem = '<p><strong>' + timestamp + '</strong>: ' + message + '</p>';
                    $('#logContainer').append(logItem);
                }

                lastTimestamp = newLogs[newLogs.length - 1].timestamp;

                var logContainer = document.getElementById('logContainer');
                logContainer.scrollTop = logContainer.scrollHeight;
            }
        }).always(function() {
            requestFlag = true;
        });
    }

    getLogs();
    setInterval(getLogs, 5000);



// Функции действий
function force() {
    var resultContainer = document.getElementById('result');
    var salonid = document.getElementById('salon_id').value;

    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/rsafe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'salon': salonid
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            displaySuccessMessage(data.text);
            resultContainer.innerHTML = "";
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);
            resultContainer.innerHTML = "";
        }
    })
}

function savedb() {
    var resultContainer = document.getElementById('result');
    var salonid = document.getElementById('salon_id').value;

    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/safeshedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'salon': salonid
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            resultContainer.innerHTML = "";
            displaySuccessMessage(data.text);
        } else if (data.status === 'error') {
            displayErrorMessage(data.text);
            resultContainer.innerHTML = "";
        }
    })
}


function clearSh() {
    var resultContainer = document.getElementById('result');
    var salonid = document.getElementById('salon_id').value;

    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/clearshedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'salon': salonid
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            resultContainer.innerHTML = "";
            displaySuccessMessage(data.text);
        } else if (data.status === 'error') {
            resultContainer.innerHTML = "";
            displayErrorMessage(data.text);
        }
    })
}


function repair() {
    var resultContainer = document.getElementById('result');
    var salonid = document.getElementById('salon_id').value;

    resultContainer.innerHTML = '<div class="loader"><i class="fa fa-spinner fa-spin"></i> Ждем...</div>';

    return fetch('/repairshedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'salon': salonid
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            resultContainer.innerHTML = "";
            displaySuccessMessage(data.text);
        } else if (data.status === 'error') {
            resultContainer.innerHTML = "";
            displayErrorMessage(data.text);
        }
    })
}