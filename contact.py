import json

from flask import Blueprint, request, jsonify
from datetime import datetime
from slack_sdk import WebClient

from config import slack_token

api_token = slack_token
channel = 'C05AHHXKB6C'

feedback = Blueprint('feedback', __name__)
wishes_file = "wishes.txt"

@feedback.route('/submit_feedbacmmk', methods=['POST'])
def submit_feedback():
    feedback_text = request.json['text']
    hide_checkbox = request.json['hide']
    feedback = {
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'text': feedback_text,
        'hide': 1 if hide_checkbox else 0
    }
    with open('wishes.txt', 'a') as file:
        file.write(json.dumps(feedback) + '\n')
    send_to_slack(feedback)
    return jsonify({'success': True})

def send_to_slack(feedback):
    text = feedback['text']
    hide = feedback['hide']
    hide_text = "Да" if hide else "Нет"
    message = f''':warning: *НОВЫЙ ОТЗЫВ* :warning:\n*Текст:* {text}\n*Анонимный:* {hide_text}'''

    client = WebClient(token=api_token)
    response = client.chat_postMessage(channel=channel, text=message)
    assert response["message"]["text"] == message, response

    return response


@feedback.route('/get_feedback', methods=['GET'])
def get_feedback():
    feedback_list = read_feedback()
    return jsonify(feedback_list)

def read_feedback():
    feedback_list = []
    with open(wishes_file, 'r') as file:
        for line in file:
            feedback = json.loads(line.strip())
            feedback_list.append(feedback)
    return [feedback for feedback in feedback_list if feedback['hide'] == 0]
