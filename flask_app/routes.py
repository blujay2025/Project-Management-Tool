from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################

# Gets the user from a browser session
def getUser():
    return session['email'] if 'email' in session else 'Unknown'


# Renders login page
@app.route('/login')
def login():
    return render_template('login.html')


# Renders account creation page
@app.route('/create-account')
def create_account():
    return render_template('create-account.html')


# Pops email from browser session and re-directs back to home page
@app.route('/logout')
def logout():
    session.pop('email', default=None)
    return redirect('/')

# Processes the login action for a user
@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    form_email = request.form.get('email')
    form_password = request.form.get('password')

    auth_result = db.authenticate(email=form_email, password=form_password)

    if auth_result['success'] == 1:
        session['email'] = form_email
        return json.dumps({'success': 1})
    else:
        return json.dumps({'success': 0})


#######################################################################################
# BOARD RELATED
#######################################################################################

# Renders projects option page
@app.route('/projects')
def projects():
    return render_template('projects.html')


# Renders board creation page
@app.route('/board-creation')
def board_creation():
    return render_template('board-creation.html')


# Renders existing boards for a particular user
@app.route('/existing-boards')
def existing_boards():
    result_list = db.query(
        "SELECT * FROM projects WHERE email = %s", (getUser(),))

    return render_template('existing-boards.html', existing_projects_list=result_list)


# Creates the account for a user
@app.route('/accountcreation', methods=["POST", "GET"])
def accountcreation():
    form_email = request.form.get('email')
    form_password = request.form.get('password')

    user_list = db.query("SELECT * FROM users WHERE email = %s", (form_email,))

    if len(user_list) > 0:
        return redirect('/create-account')

    hashed_password = db.onewayEncrypt(form_password)

    db.insertRows('users', ['email', 'password'],
                  [[form_email], [hashed_password]])

    return render_template('home.html')


# Creates the board for a project
@app.route('/boardcreationprocess', methods=["POST", "GET"])
def boardcreationprocess():

    project_name = request.form.get('boardname')
    member_count = int(request.form.get('memberIdCount'))

    db.insertRows('projects', ['email', 'project_name'], [
                  [getUser()], [project_name]])

    counter = 1

    while counter <= member_count:
        request_string = "member" + str(counter)
        member_email = request.form.get(request_string)
        db.insertRows('projects', ['email', 'project_name'], [
                      [member_email], [project_name]])
        counter += 1

    return redirect(f'/board/{project_name}')


# Updates the cards table with the right information
@app.route('/cardstableupdate', methods=["POST", "GET"])
def cardstableupdate():
    command_type = request.form.get('request_type')
    project_name = request.form.get('project_name')
    status = request.form.get('status')
    card_content = request.form.get('card_content')
    if request.form.get('card_id') != None:
        card_id = int(request.form.get('card_id'))

    if command_type == "INSERT":
        card_id = db.insertRows('cards', ['status', 'project_name', 'card_content'],
                    [[status], [project_name], [card_content]])
        return json.dumps({'success': 1, "card_id": card_id})
    else:
        db.query("UPDATE cards SET card_content = %s WHERE card_id = %s",
                 (card_content, card_id))
        return json.dumps({'success': 1})


# Checks if a card within a particular list with the same content already exists, if so the card gets deleted
@app.route('/card-already-exists', methods=["POST", "GET"])
def cardexists():
    project_name = request.form.get('project_name')
    status = request.form.get('status')
    card_content = request.form.get('card_content')

    card_list = db.query("SELECT * FROM cards WHERE project_name = %s AND status = %s AND card_content = %s",
                         (project_name, status, card_content))

    if len(card_list) == 0:
        return json.dumps({'success': 1})
    else:
        return json.dumps({'success': 0})
    

# Deletes a card given a card's id
@app.route('/deletecard', methods=["POST", "GET"])
def deletecard():
    card_id = int(request.form.get('card_id'))

    db.query("DELETE FROM cards WHERE card_id = %s",
             (card_id,))
    
    return json.dumps({'success': 1})


# Updates on drag and drop
@app.route('/draganddropupdate', methods=["POST", "GET"])
def draganddropupdate():
    project_name = request.form.get('project_name')
    old_card_id = request.form.get('old_card_id')
    new_status = request.form.get('new_status')

    db.query("UPDATE cards SET status = %s WHERE project_name = %s AND card_id = %s",
             (new_status, project_name, old_card_id))

    return json.dumps({'success': 1})


# Routes to a particular project board
@app.route('/board/<projectName>')
def boardProjection(projectName):
    project_info = db.query(
        "SELECT * FROM projects WHERE email = %s AND project_name = %s", (getUser(), projectName))

    if not project_info:
        auth_result = {'success': 0}
    else:
        auth_result =  {'success': 1}

    if auth_result['success'] == 0:
        return redirect('/login')
    else:
        result_list = db.query(
            "SELECT * FROM cards WHERE project_name = %s ORDER BY card_id", (projectName,))
        return render_template('board.html', board_name=projectName, card_list=result_list)


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat/<chatRoom>')
# Takes user to a particular chat room associated with a particular project
def chat(chatRoom):
    project_info = db.query(
        "SELECT * FROM projects WHERE email = %s AND project_name = %s", (getUser(), chatRoom))

    if not project_info:
        auth_result = {'success': 0}
    else:
        auth_result =  {'success': 1}

    if auth_result['success'] == 0:
        return redirect('/login')
    else:
        return render_template('chat.html', board_name=chatRoom)


# Allows a user to join a board
@socketio.on('join_board', namespace='/')
def join_board(data):
    join_room(data['projectName'])
    emit('status', {'msg': getUser() + ' has entered the room.'},
         room=data['projectName'])


# Emits a message to the board
@socketio.on('message', namespace='/')
def message(data):
    emit('message', {'msg': data['msg'],
         'user': getUser()}, room=data['roomName'])


# Allows user to leave a chat room
@socketio.on('left', namespace='/')
def left(data):
    leave_room(data['roomName'])
    emit('status', {'msg': getUser() + ' has left the room.'},
         room=data['roomName'])


#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
    return redirect('/home')


# Routes user home
@app.route('/home')
def home():
    return render_template('home.html')