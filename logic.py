# -*- coding: utf-8 -*-
import re
import random


def dice(body: str, selfUserName: str = "@DiceBot") -> str:
    # bodyの文字列の数値を変換
    body = body.replace("　", " ")
    body = body.replace("１", "1")
    body = body.replace("２", "2")
    body = body.replace("３", "3")
    body = body.replace("４", "4")
    body = body.replace("５", "5")
    body = body.replace("６", "6")
    body = body.replace("７", "7")
    body = body.replace("８", "8")
    body = body.replace("９", "9")
    body = body.replace("０", "0")

    # bodyの文字列を で分割する
    words = body.split(" ");

    print("s:", words)

    # 数値を取得する
    number = None
    for iter in words:
        if re.search(selfUserName, iter) == None and re.search("\d+([dDＤ]\d+)?", iter):
            number = re.search("\d+([dDＤ]\d+)?", iter).group(0)
            break
    # 取得できなかった場合は最大数を6にする
    if number == None:
        number = "6"

    print("number:", number)

    try:

        try:
            try:
                # TRPG用表記
                # print "TRPG用の表記です"
                x = int(re.search(r"(\d+)[dDＤ](\d+)", number).group(1))
                r = int(re.search(r"(\d+)[dDＤ](\d+)", number).group(2))
            except:
                raise

        except:

            # 乱数を決定する
            # print "乱数を取得しています"
            r = re.search(r"\d+", number).group()
            # print "r: "+r


            # 繰り返す回数
            try:
                # print "xで繰り返す回数を取得しています"
                x = int(re.search(r"x(\d+)", number).group(1))
                # print "x: "+str(x)
            except:
                try:
                    # print "×で繰り返す回数を取得しています"
                    x = int(re.search(r"×(\d+)", number).group(1))
                    # print "x: "+str(x)
                except:
                    x = 1

        # 1または1より低い場合はslotを1にする
        if int(r) == 0 and x == 0:

            # print "全て0です"
            slot = "0"

        else:

            # xが0より下だった場合
            if x < 0:
                # print "xが0より下です"
                raise

            # rが0より下だった場合
            if int(r) < 0:
                # print "rが0より下です"
                raise

            # 1以下だった場合
            if int(r) <= 1:
                # print "1以下です"
                slot = ""
                # print str(x)+"回繰り返します"
                for i in range(x):
                    # print "繰り返し中: "+str(i)
                    if int(i) > 0:
                        # print "、を追加しています"
                        slot += "、"
                    # print "slotを追加しています"
                    slot += r
                    # print ""+slot

            else:
                # 数値が1以上の場合
                try:
                    # print "1以上です"
                    # ランダムに決定する
                    slot = ""
                    # print "繰り返します"
                    for i in range(x):
                        if int(i) > 0:
                            # print "slotに追加しています"
                            slot += "、"
                        # print "slotに追加します"
                        slot += str(random.randint(1, int(r)))
                        # print ""+slot
                except:
                    # 例外を引き渡す
                    # print "エラーが発生しました"
                    raise

    except:
        # エラーが発生した場合は 1〜6 の範囲にする
        slot = str(random.randint(1, 6))

    # 文字を修正する
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

    return "サイコロの目は『{0}』でした。".format(str(slot))
