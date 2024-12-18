from flask import request, jsonify
from models.Chat import ChatModel, MessageModel, VoteModel
import datetime
from database import db

from ControllerRAG import getFinalResponse
def sendPrompt():
    prompt = request.get_json()
    print(prompt)
    message = getFinalResponse(prompt)
    return jsonify({'message': message})


def vote():
    if request.method == 'GET':
        print('GET')
        return jsonify({'method': 'GET'})
    if request.method == 'PATCH':
        print('PATCH')
        return jsonify({'method': 'PATCH'})


def voteMessage():
    data = request.get_json()
    vote = VoteModel.query.filter_by(messageId=data['messageId'], chatId=data['chatId']).first()
    print(vote)
    return jsonify(vote.serialize)


def getVotesByChatId():
    args = request.args
    print(request.args)
    votes = VoteModel.query.filter_by(chatId=args['chatId']).all()
    return [i.serialize for i in votes]


def generateTitleFromUserMessage(message):
    return 'title'


def saveChat(user_id):
    data = request.get_json()
    message = data['message']
    titleMessage = generateTitleFromUserMessage(message)
    new_chat = ChatModel(
                userId=user_id,
                title=titleMessage,
                createdAt=datetime.datetime.now(datetime.UTC)
            )
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({'status': 'success'})


def saveMessages():
    data = request.get_json()
    messages = [
                MessageModel(
                   chatId=message['chatId'],
                   role=message['role'],
                   content=message['content'],
                   createdAt=datetime.datetime.utcfromtimestamp(float(message['createdAt']))
                )
                for message in data
            ]
    db.session.add_all(messages)
    db.session.commit()
    return jsonify({'status': 'success'})


def deleteChatById():
    chat_id = request.args['id']
    vote = db.session.query(VoteModel).filter_by(chatId=chat_id).delete(synchronize_session=False)
    messages = db.session.query(MessageModel).filter_by(chatId=chat_id).delete(synchronize_session=False)
    db.session.query(ChatModel).filter_by(id=chat_id).delete(synchronize_session=False)
    db.session.commit()
    return 'chat deleted'


def getChatsByUserId(user_id):
    chats = ChatModel.query.filter_by(userId=user_id).all()
    return jsonify([chat.serialize for chat in chats])


def getChats():
    chats = ChatModel.query.all()
    return jsonify([i.serialize for i in chats])


def getChatById(chat_id):
    chat = ChatModel.query.filter_by(id=chat_id).first()
    return jsonify(chat.serialize)


def getMessageById(message_id):
    return 'messages'


def getMessagesByChatId(chat_id):
    messages = MessageModel.query.filter_by(chatId=chat_id).all()
    return jsonify([i.serialize for i in messages])


def updateVisibilityById(chat_id):
    return 'vvisibility updated'
