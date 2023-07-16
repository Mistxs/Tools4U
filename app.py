from flask import Flask, render_template, request, jsonify
from fsr import fsr
from unlocker import unlocker
from superloyalty import superloya
from TrackerSearch import tsearch
from contact import feedback
from getcookie import ucookie
from overpayed import overpay
from superday import superday
from DSlotsRepair import dslots
from fiosplitter import fiosplitter

# from resafe import *
import re

app = Flask(__name__)

# Регистрация приложений
app.register_blueprint(fsr)
app.register_blueprint(unlocker)
app.register_blueprint(superloya)
app.register_blueprint(tsearch)
app.register_blueprint(feedback)
app.register_blueprint(ucookie)
app.register_blueprint(overpay)
app.register_blueprint(superday)
app.register_blueprint(dslots)
app.register_blueprint(fiosplitter)



# Роуты для вебстраниц (не действий)
@app.route('/start')
def start():
    title = 'Стартовая'
    active_page = 'start'
    return render_template('start.html', title=title, active_page=active_page)

@app.route('/')
def index():
    title = 'Force Save Result'
    active_page = 'fsr'
    return render_template('fsr.html', title=title, active_page=active_page)

@app.route('/fsr')
def fsr():
    title = 'Force Save Result'
    active_page = 'fsr'
    return render_template('fsr.html', title=title, active_page=active_page)

@app.route('/superloyal')
def superloyal():
    title = 'Подробная лояльность (супер карта лояльности)'
    active_page = 'superloyal'
    return render_template('superloyal.html', title=title, active_page=active_page)

@app.route('/finance')
def finance():
    title = 'Поиск переплат'
    active_page = 'finance'
    return render_template('finance.html', title=title, active_page=active_page)

@app.route('/unlock')
def unlocker():
    title = 'Разблокировка визитов'
    active_page = 'unlocker'
    return render_template('unlocker.html', title=title, active_page=active_page)

@app.route('/inna')
def inna():
    title = 'InnaBot - самый дружелюбный бот'
    active_page = 'inna'
    return render_template('inna.html', title=title, active_page=active_page)

@app.route('/search')
def tracker():
    title = 'Поиск по трекеру'
    active_page = 'search'
    return render_template('tsearch.html', title=title, active_page=active_page)


@app.route('/feedback')
def fdb():
    title = 'Обратная связь'
    active_page = 'feedback'
    return render_template('feedback.html', title=title, active_page=active_page)

@app.route('/getcookie')
def getcookie():
    title = 'Get Cookie from kibana'
    active_page = 'start'
    return render_template('getcookie.html', title=title, active_page=active_page)

@app.route('/daydetails')
def overpayed():
    title = 'Детальный просмотр записей за день'
    active_page = 'start'
    return render_template('superday.html', title=title, active_page=active_page)

@app.route('/repairslots')
def repairslots():
    title = 'Пересохранение расписания'
    active_page = 'dslots'
    return render_template('dslots.html', title=title, active_page=active_page)

@app.route('/fiosplitter')
def fio():
    title = 'Сплиттер Имени на ФИО'
    active_page = 'fiosplit'
    return render_template('fiosplitter.html', title=title, active_page=active_page)



if __name__ == '__main__':
    app.run(port=3000)