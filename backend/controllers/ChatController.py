from flask import request, jsonify, make_response
from models.Chat import ChatModel, MessageModel, VoteModel
import datetime
from database import db
from controllers.ControllerRAG import getFinalResponse
from controllers.GenerateTitle import getTitle


def sendPrompt():
    req = request.get_json()
    data = req['message']
    user_id = req['userId']
    chat = ChatModel.query.filter_by(id=data['chatId']).first()
    print("chat is")
    print(chat)
    if (chat is None):
        print("no chat")
        message = data['content']
        titleMessage = getTitle(message)
        new_chat = ChatModel(
                    id=data['chatId'],
                    userId=user_id,
                    title=titleMessage,
                    createdAt=datetime.datetime.now(datetime.UTC)
                )
        print("new Chat")
        print(new_chat)
        db.session.add(new_chat)

    response = getFinalResponse(data['content'])
    print("message response")
    print(response)
    # response = "hello there"
    messageResponse = MessageModel(
            chatId=data['chatId'],
            role='assistant',
            content=[{
                "text": response,
                "type": "text"
                }
                     ],
            createdAt=datetime.datetime.utcnow()
            )
    print("message response serialize")
    print(messageResponse.serialize)
    messagePrompt = MessageModel(
            id=data['id'],
            chatId=data['chatId'],
            role=data['role'],
            content=data['content'],
            createdAt=data['createdAt']
            )
    db.session.add_all([messagePrompt, messageResponse])
    db.session.commit()
    return jsonify({'message': messageResponse.serialize})


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
    try:
        chat = ChatModel.query.filter_by(id=chat_id).first()
        return jsonify(chat.serialize)
    except Exception:
        return make_response(
                {'error': 'not found'},
                404
             )


def getMessageById(message_id):
    return 'messages'


def getMessagesByChatId(chat_id):
    messages = MessageModel.query.filter_by(chatId=chat_id).all()
    return jsonify([i.serialize for i in messages])


def updateVisibilityById(chat_id):
    return 'vvisibility updated'
