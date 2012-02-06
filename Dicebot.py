#!/home/nacika/.virtualenvs/akicansoft/bin/python
# -*- coding: utf-8 -*-
import codecs
import google
import logging
import random
import simplejson as json
import sys
import threading
import time
import traceback
import re

def addjson(_filepath, _json, _code="utf-8"):
    try:
        f = codecs.open(_filepath, "r+", _code)
    except:
        try:
            f = codecs.open(_filepath, "w", _code)
            f.write("")
        except:
            return 0

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
        return 1
    except:
        try:
            f.close()
        except:
            return 1

class _dicepost(threading.Thread):
    def __init__(self, _ID, _body, _post, _postid):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.post = _post
        self.postid = _postid
        self.body = _body
        self.loglist = []
        self.ID = _ID
        
    def run(self):

        
        #bodyの文字列の数値を変換
        self.body = self.body.replace("　", " ")
        self.body = self.body.replace("１", "1")
        self.body = self.body.replace("２", "2")
        self.body = self.body.replace("３", "3")
        self.body = self.body.replace("４", "4")
        self.body = self.body.replace("５", "5")
        self.body = self.body.replace("６", "6")
        self.body = self.body.replace("７", "7")
        self.body = self.body.replace("８", "8")
        self.body = self.body.replace("９", "9")
        self.body = self.body.replace("０", "0")
        
        #bodyの文字列を で分割する
        s = self.body.split(" ");
        
        #数値を取得する
        flag = 0
        for i in s:
            if flag == 1:
                s = i
                break
            try:
                if re.search("oid=\"%s\">(.+)</a></span>" % self.ID, i).group(1):
                    flag = 1
            except:
                pass

        
        #取得できなかった場合は最大数を6にする
        if flag == 0:
            s = "6"
        
        #print "s: " + s

        try:
            
            try:
                try:
                    #TRPG用表記
                    #print "TRPG用の表記です"
                    x = int(re.search(r"(\d+)[dDＤ](\d+)", s).group(1))
                    r = int(re.search(r"(\d+)[dDＤ](\d+)", s).group(2))
                except:
                    raise

            except:
                
                #乱数を決定する
                #print "乱数を取得しています"
                r = re.search(r"\d+", s).group()
                #print "r: "+r
                
                
                #繰り返す回数
                try:
                    #print "xで繰り返す回数を取得しています"
                    x = int(re.search(r"x(\d+)", s).group(1))
                    #print "x: "+str(x)
                except:
                    try:
                        #print "×で繰り返す回数を取得しています"
                        x = int(re.search(r"×(\d+)", s).group(1))
                        #print "x: "+str(x)
                    except:
                        x = 1
                        
                    
            
            #1または1より低い場合はslotを1にする
            if int(r) == 0 and x == 0:
                
                #print "全て0です"
                slot = "0"
                
            else:
                
                
                #xが0より下だった場合
                if x < 0:
                    #print "xが0より下です"
                    raise
                
                #rが0より下だった場合
                if int(r) < 0:
                    #print "rが0より下です"
                    raise
                
                #1以下だった場合
                if int(r) <= 1:
                    #print "1以下です"
                    slot = ""
                    #print str(x)+"回繰り返します"
                    for i in range(x):
                        #print "繰り返し中: "+str(i)
                        if int(i) > 0:
                            #print "、を追加しています"
                            slot += "、"
                        #print "slotを追加しています"
                        slot += r
                        #print ""+slot
                        
                else:
                    #数値が1以上の場合    
                    try:
                        #print "1以上です"
                        #ランダムに決定する
                        slot = ""
                        #print "繰り返します"
                        for i in range(x):
                            if int(i) > 0:
                                #print "slotに追加しています"
                                slot += "、"
                            #print "slotに追加します"
                            slot += str(random.randint(1, int(r)))
                            #print ""+slot
                    except:
                        #例外を引き渡す
                        #print "エラーが発生しました"
                        raise
                    
        except:
            #エラーが発生した場合は 1〜6 の範囲にする
            slot = str(random.randint(1, 6))
            
        #文字を修正する
        slot = slot.replace("1", "１")
        slot = slot.replace("2", "２")
        slot = slot.replace("3", "３")
        slot = slot.replace("4", "４")
        slot = slot.replace("5", "５")
        slot = slot.replace("6", "６")
        slot = slot.replace("7", "７")
        slot = slot.replace("8", "８")
        slot = slot.replace("9", "９")
        slot = slot.replace("0", "０")

        
        
        try:
            #print "エラーが発生しました"
            #print "サイコロを振ります。"
            self.post.comment(self.postid, "*サイコロの目は、『" + str(slot) + "』でした。*")
        except:
            #print "投稿に失敗しました"
            pass
 


#ダイスを投稿するか判断する
def dicepost(_ID, _post, _postid, _body):

        try:
            _body.index(_ID)
            #print "ダイスを投稿します"
            
            _dicepost(_ID, _body, _post, _postid).start()
            
            #10秒待つ
            #print "30秒待機しています"
            time.sleep(30)
            return 1
        except:
            return 0

def main():
    
    ID = "112798774609070880358" #Release
    #ID = "107783647697859888499" #Debug


    #投稿ログの読み込み
    try:
        #print "投稿ログを読み込んでいます"
        f = open("/home/nacika/bot/Dicebot/postlog.txt", "r+")
        postlog = json.load(f)
    except:
        try:
            #print "新規投稿ログを作成し開いています"
            f = open("/home/nacika/bot/Dicebot/postlog.txt", "w")
            f.write("")
            postlog = []
        except:
            try:
                #print "デバッグ用postlog.txtを開いています"
                f = open("postlog.txt", "r+")
                postlog = json.load(f)
            except:
                #print "デバッグ用postlog.txtを新規オープンしています"
                f = open("postlog.txt", "w")
                f.write("")
                postlog = []
    try:
        f.close()
    except:
        pass
        

    #ログイン
    #print "Googleにログインしています"
    g = google.Login("", "")
    plus = g.plus(ID)
    post = plus.post()
    
    #ループ
    while 1:
        #通知があるか確認する
        #print "通知があるか確認しています"
        if plus.notifycheck():
            #print "通知を取得しています"
            notify = plus.notify()
            size = notify.length()
            #print "通知が%d件ありました" % size

            
            #通知の回数だけ繰り返す
            for i in range(size)[::-1]:
                
                body = notify.postbody(i)
                postid = notify.postid(i)
                
                #削除されたポストは無視
                if postid == "":
                    continue
                
                #ログのチェック
                flag = 0
                for c in postlog:
                    if postid == c:
                        
                        #すでに投稿されている
                        #print "すでに投稿されているポストです: " + postid
                        flag = 1
                        break
                
                #重複がない場合実行
                if not flag:
                    
                    
                    if dicepost(ID, post, postid, body):
                        
                        #投稿された
                        postlog.append(postid)
                        #print "ポストログを追加しています"
                        addjson("/home/nacika/bot/Dicebot/postlog.txt", json.dumps(postid))
                
                #コメントの取得
                for ii in range(notify.commentlength(i)):
                    
                    body = notify.commentbody(i, ii)
                    comid = notify.commentid(i, ii)
                    
                    try:
                        #print "コメントを取得しています"
                        #print "本文: " + body
                        #print "コメントID: " + comid
                        pass
                    except:
                        pass
                    
                    #ログのチェック
                    #print "コメントログのチェックを行なっています"
                    flag = 0
                    for c in postlog:
                        if comid == c:
                            flag = 1
                            break
                    if flag:
                        #print "すでに投稿されているコメントです: " + comid
                        continue
                    
                    if dicepost(ID, post, postid, body):
                        
                        #投稿された
                        postlog.append(comid)
                        #print "ポストログを追加しています"
                        try:
                            addjson("/home/nacika/bot/Dicebot/postlog.txt", json.dumps(comid))
                        except:
                            addjson("postlog.txt", json.dumps(comid))
                        
    
   
        #2分更新
        #print "2分待機中"
        time.sleep(60 * 2)
        #print "2分経過しました"

        

if __name__ == '__main__':
    while 1:
        try:
            main()
        except:
            info = sys.exc_info()
            tbinfo = traceback.format_tb(info[2])
            for tbi in tbinfo:
                logging.error(tbi)
            logging.error("%s\n-----------------------------------------------" % str(info[1]))
            time.sleep(60 * 10)
            continue
