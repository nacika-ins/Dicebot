# -*- coding: utf-8 -*-
import codecs
import simplejson as json
import sys
from urllib.parse import urlparse
import requests
import json
import websocket
import logic
from mastodon import Mastodon

API_BASE_URL = "https://oransns.com"
LOGIN_MAILADDRESS = 'nacika.inscatolare+dicebot@gmail.com'
LOGIN_PASSWORD = """X#u='LRY'L_"B5c~5(Vacx&,:g|!+r7b"""


# jsonに追加する
def addjson(_filepath, _json, _code="utf-8"):
    try:
        f = codecs.open(_filepath, "r+", _code)
    except:
        try:
            f = codecs.open(_filepath, "w", _code)
            f.write("")
        except:
            pass

    try:
        try:
            s = f.read(2)
            if s == "":
                b = "["
            elif s == "[]":
                b = ""
            else:
                b = ","

            if s == "":
                pass
            else:
                f.seek(-1, 2)
        except:
            b = "["

        f.write(u"" + b + _json + "]")
        f.close()
    except:
        try:
            f.close()
        except:
            pass


class MstdnStreamListner:
    def on_update(self, data):
        print(data)

    def on_notification(self, data):
        print(data)

    def on_delete(self, data):
        print("Deleted: {id}".format(id=data))


class MstdnStream:
    def __init__(self, base_url: str, access_token: str, listener: MstdnStreamListner, mastodon: Mastodon):
        self.base_url = base_url
        self.access_token = access_token
        self.session = requests.Session()
        self.mastodon = mastodon
        self.session.headers.update({
            'Authorization': 'Bearer ' + access_token,
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Key': 'OzqJNi0KGlFSCqIyrScjnA=='
        })
        self.listener = listener

    def user(self):

        # create url
        # url = urljoin(self.base_url, '/api/v1/streaming/?access_token=' + self.access_token + "&stream=user")
        # print("url: ", url)


        # websocket
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            "wss://oransns.com/api/v1/streaming/?access_token=" + self.access_token + "&stream=user",
            header=["Authorization: Bearer %s" % self.access_token],
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close
        )

        # websocketを起動する。Ctrl+Cで終了するようにする。
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()

    # ここで定義したメソッドがwebsocketのコールバック関数になる。
    # messageをうけとったとき
    def __on_message(self, ws, message):

        try:
            # {"event":"notification","payload":"{\"id\":19988,\"type\":\"mention\",\"created_at\":\"2017-04-22T07:24:22.892Z\",\"account\":{\"id\":1,\"username\":\"nacika\",\"acct\":\"nacika\",\"display_name\":\"nacika inscatolare(沼)🇳🇱\",\"locked\":false,\"created_at\":\"2017-04-13T12:14:01.595Z\",\"followers_count\":233,\"following_count\":298,\"statuses_count\":1343,\"note\":\"<a href=\\\"https://oransns.com\\\" rel=\\\"nofollow noopener\\\" target=\\\"_blank\\\"><span class=\\\"invisible\\\">https://</span><span class=\\\"\\\">oransns.com</span><span class=\\\"invisible\\\"></span></a> を管理するぴちょんくん\",\"url\":\"https://oransns.com/@nacika\",\"avatar\":\"https://oransns.com/system/accounts/avatars/000/000/001/original/cad1912466f9f3e9.GIF?1492396068\",\"avatar_static\":\"https://oransns.com/system/accounts/avatars/000/000/001/static/cad1912466f9f3e9.png?1492396068\",\"header\":\"https://oransns.com/system/accounts/headers/000/000/001/original/951ba2b8a22abbd1.GIF?1492396070\",\"header_static\":\"https://oransns.com/system/accounts/headers/000/000/001/static/951ba2b8a22abbd1.png?1492396070\"},\"status\":{\"id\":274652,\"created_at\":\"2017-04-22T07:24:22.822Z\",\"in_reply_to_id\":null,\"in_reply_to_account_id\":null,\"sensitive\":false,\"spoiler_text\":\"\",\"visibility\":\"public\",\"application\":null,\"account\":{\"id\":1,\"username\":\"nacika\",\"acct\":\"nacika\",\"display_name\":\"nacika inscatolare(沼)🇳🇱\",\"locked\":false,\"created_at\":\"2017-04-13T12:14:01.595Z\",\"followers_count\":233,\"following_count\":298,\"statuses_count\":1343,\"note\":\"<a href=\\\"https://oransns.com\\\" rel=\\\"nofollow noopener\\\" target=\\\"_blank\\\"><span class=\\\"invisible\\\">https://</span><span class=\\\"\\\">oransns.com</span><span class=\\\"invisible\\\"></span></a> を管理するぴちょんくん\",\"url\":\"https://oransns.com/@nacika\",\"avatar\":\"https://oransns.com/system/accounts/avatars/000/000/001/original/cad1912466f9f3e9.GIF?1492396068\",\"avatar_static\":\"https://oransns.com/system/accounts/avatars/000/000/001/static/cad1912466f9f3e9.png?1492396068\",\"header\":\"https://oransns.com/system/accounts/headers/000/000/001/original/951ba2b8a22abbd1.GIF?1492396070\",\"header_static\":\"https://oransns.com/system/accounts/headers/000/000/001/static/951ba2b8a22abbd1.png?1492396070\"},\"media_attachments\":[],\"mentions\":[{\"url\":\"https://oransns.com/@QuizBot\",\"acct\":\"QuizBot\",\"id\":12099,\"username\":\"QuizBot\"}],\"tags\":[],\"uri\":\"tag:oransns.com,2017-04-22:objectId=274652:objectType=Status\",\"content\":\"<p><span class=\\\"h-card\\\"><a href=\\\"https://oransns.com/@QuizBot\\\" class=\\\"u-url mention\\\">@<span>QuizBot</span></a></span> test</p>\",\"url\":\"https://oransns.com/@nacika/274652\",\"reblogs_count\":0,\"favourites_count\":0,\"reblog\":null,\"favourited\":false,\"reblogged\":false}}"}
            # {"id":295757,"created_at":"2017-04-22T20:03:34.432Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"public","application":null,"account":{"id":1,"username":"nacika","acct":"nacika","display_name":"nacika inscatolare(沼)🇳🇱","locked":false,"created_at":"2017-04-13T12:14:01.595Z","followers_count":237,"following_count":304,"statuses_count":1467,"note":"<a href=\"https://oransns.com\" rel=\"nofollow noopener\" target=\"_blank\"><span class=\"invisible\">https://</span><span class=\"\">oransns.com</span><span class=\"invisible\"></span></a> を管理するぴちょんくん","url":"https://oransns.com/@nacika","avatar":"https://oransns.com/system/accounts/avatars/000/000/001/original/cad1912466f9f3e9.GIF?1492396068","avatar_static":"https://oransns.com/system/accounts/avatars/000/000/001/static/cad1912466f9f3e9.png?1492396068","header":"https://oransns.com/system/accounts/headers/000/000/001/original/951ba2b8a22abbd1.GIF?1492396070","header_static":"https://oransns.com/system/accounts/headers/000/000/001/static/951ba2b8a22abbd1.png?1492396070"},"media_attachments":[],"mentions":[{"url":"https://oransns.com/@QuizBot","acct":"QuizBot","id":12099,"username":"QuizBot"}],"tags":[],"uri":"tag:oransns.com,2017-04-22:objectId=295757:objectType=Status","content":"<p><span class=\"h-card\"><a href=\"https://oransns.com/@QuizBot\" class=\"u-url mention\">@<span>QuizBot</span></a></span> ssss</p>","url":"https://oransns.com/@nacika/295757","reblogs_count":0,"favourites_count":0,"reblog":null,"favourited":false,"reblogged":false}
            data = json.loads(message)
            payload = data["payload"]
            payload_data = json.loads(payload)

            print(payload_data)

            # 通知 かつ メンションの場合のみ
            if data["event"] == "notification" and payload_data["type"] == "mention":
                user_name = payload_data["account"]["username"]
                url = payload_data["account"]["url"]
                domain = urlparse(url).netloc
                reply_id = payload_data["status"]["id"]
                user_id = "@" + user_name + "@" + domain
                content = payload_data["status"]["content"]

                body = user_id + " " + logic.dice(content)

                response = self.mastodon.status_post(
                    status=body,
                    in_reply_to_id=reply_id,
                    visibility="public"
                )

        except Exception as e:
            print("json parse error: ", e)

    # エラーが起こった時
    def __on_error(self, ws, error):
        print(error)

    # websocketを閉じた時
    def __on_close(self, ws):
        print('disconnected streaming server')

    # websocketを開いた時
    def __on_open(self, ws):
        print('connected streaming server')


def main():
    argvs = sys.argv
    print(argvs)

    # init
    if len(argvs) >= 2 and argvs[1] == "init":
        init()

    # login
    if len(argvs) >= 2 and argvs[1] == "login":
        login()

    # quiz
    else:
        stream()


# login
def login():
    mastodon = Mastodon(
        client_id='pytooter_clientcred.txt',
        api_base_url=API_BASE_URL
    )
    access_token = mastodon.log_in(
        username=LOGIN_MAILADDRESS,
        password=LOGIN_PASSWORD,
        to_file='pytooter_usercred.txt'
    )
    print(access_token)


# quiz
def stream():
    mastodon = Mastodon(
        client_id='pytooter_clientcred.txt',
        api_base_url=API_BASE_URL
    )
    access_token = mastodon.log_in(
        LOGIN_MAILADDRESS,
        LOGIN_PASSWORD,
        to_file='pytooter_usercred.txt'
    )
    listener = MstdnStreamListner()
    stream = MstdnStream(API_BASE_URL, access_token, listener, mastodon)
    stream.user()


# 初期化
def init():
    # 一度だけ実行
    Mastodon.create_app(
        "quizbot",
        to_file="pytooter_clientcred.txt",
        api_base_url=API_BASE_URL
    )
    print("created pytooter_clientcred.txt")
    exit(0)


# main
if __name__ == '__main__':
    main()
