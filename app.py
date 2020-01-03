from flask import Flask, jsonify, request
from flask.json import JSONEncoder
class CustomJSONEncoder(JSONEncoder):
    def default(self,obj):
        if isinstance(obj,set):
            return list(obj)
        return JSONEncoder.default(self,obj)
    

app = Flask(__name__)
app.users ={}
app.id_count = 1
app.tweets=[]
app.json_encoder = CustomJSONEncoder

@app.route("/ping",methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up",methods=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count +1
    return jsonify(new_user)

@app.route("/tweet",methods=['POST'])
def write():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return '사용자가 존재하지 않습니다.',400
    if len(tweet) >300:
        return '300자를 초과했습니다.',400

    app.tweets.append(
        {
            'user_id': user_id,
            'tweet'  : tweet
        }
    )
    return 'OK',200

@app.route("/follow",methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    follow_id = int(payload['follow'])
    
    if user_id not in app.users:
        return '사용자가 존재하지 않습니다.', 400
    
    if follow_id not in app.users:
        return 'follow할 때상이 존재하지 않습니다.',400
    
    user = app.users[user_id]
    user.setdefault('follow',set()).add(follow_id)
    # 오류가 나는 이유 : set을 파이썬의 json모듈이 JSON으로 변경하지 못하기 때문!
    # list는 JSON으로 ㅇ변경될 수 있지만 set은 변경하지 못하므로 오류가 난다.
    # 그래서 JSON ENDCODER를 커스텀으로 만들어야함.
    return jsonify(user)

@app.route("/unfollow",methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    unfollow_id = int(payload['unfollow'])
    
    if user_id not in app.users:
        return '사용자가 존재하지 않습니다.', 400
    
    if unfollow_id not in app.users:
        return 'unfollow할 때상이 존재하지 않습니다.',400

    user = app.users[user_id]
    user.setdefault('follow',set()).discard(unfollow_id) # discard remove와 달리 삭제하고자 하는 값이 없어도 그냥 무시하고 끝남 오류를 안냄
    
    

    return jsonify(user)
