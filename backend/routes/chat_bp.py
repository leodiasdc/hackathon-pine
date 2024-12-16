from flask import Blueprint
from controllers import ChatController
from auth import token_required

chat_bp = Blueprint('chat_bp', __name__)


@chat_bp.route('/chat/prompt', methods=['POST'])
@token_required
def sendPrompt():
    return ChatController.sendPrompt()


@chat_bp.route('/vote/<chat_id>', methods=['GET'])
@token_required
def getVotesByChatId(chat_id):
    return ChatController.getVotesByChatId(chat_id)


@chat_bp.route('/vote/<message_id>', methods=['PATCH'])
@token_required
def vote(message_id):
    return ChatController.voteMessage(message_id)


@chat_bp.route('/chats', methods=['GET'])
@token_required
def getChats():
    return ChatController.getChats()


@chat_bp.route('/saveChat/<user_id>', methods=['POST'])
@token_required
def saveChat(user_id):
    return ChatController.saveChat(user_id)


@chat_bp.route('/chat', methods=['POST'])
@token_required
def createChat():
    return ChatController.vote()


@chat_bp.route('/chat/<chat_id>', methods=['GET'])
@token_required
def getChatById(chat_id):
    return ChatController.getChatById(chat_id)


@chat_bp.route('/chat/<chat_id>', methods=['DELETE'])
@token_required
def deleteChatById(chat_id):
    return ChatController.deleteChatById(chat_id)


@chat_bp.route('/messages/<chat_id>', methods=['GET'])
@token_required
def getMessagesByChatId(chat_id):
    return ChatController.getMessagesByChatId(chat_id)


@chat_bp.route('/messages', methods=['POST'])
@token_required
def saveMessages():
    return ChatController.saveMessages()
