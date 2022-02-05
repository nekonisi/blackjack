from cgitb import lookup
from distutils.version import LooseVersion
from itertools import count
from operator import truediv
from platform import win32_edition
import random

def main():
    """ 
    メイン関数
    ©nekonisi.com
    """
    playerWin = 0
    for j in range(100):
        init()

        for i in range(10000):
            game()
            deal()
            if player.fund < 0 or 1500 <= player.fund:
                break

        print("Fund " + str(player.fund))
        print("Win " + str(player.winCount))
        print("Loose " + str(player.looseCount))
        print("Draw " + str(player.drawCount))
        # print("勝率: " + str(player.winCount / (player.winCount + player.looseCount + player.drawCount)))
        print("勝率: " + str(player.winCount / (player.winCount + player.looseCount)))

        if 1500 < player.fund:
            playerWin +=1
    print("全体勝利:" + str(playerWin))

def init():
    """
    初期化
    """
    global deck
    global player
    global dealer

    # デッキクラスの初期化
    deck = DeckList()

    # PlayerおよびDealderの初期化
    player = Player()
    dealer = Dealer()



def game():
    """
    ゲームプレイ
    """
    # print("デッキのトゥルーカウント" + str(deck.trueCount()))
    # print("デッキのカウント" + str(deck.count))
    # 最初にディーラーがカードを2枚ドロー
    dealer.draw(deck.pop())
    dealer.draw(deck.pop())
    openCard = dealer.hand[0]

    # print("Open Card is " + str(openCard))

    # 次にプレイヤーがカードを2枚ドロー
    player.draw(deck.pop())
    player.draw(deck.pop())

    # マニュアルモード
    # player.openHand()
    # player.say()
    # print("cmd? Hit:1 Stand:2")
    # cmd = input()

    # while cmd == "1":
    #     player.hit(deck.pop())
    #     player.say()
    #     if (player.score > 21 or player.score == 21):
    #         break
    #     print("cmd? Hit:1 Stand:2")
    #     cmd = input()

    # オートマ（ベーシックストラテジー）
    while True:
        if player.score == 9:
            if 3 <= openCard.num <= 6:
                player.double(deck.pop())
            else:
                player.hit(deck.pop())
        elif player.score == 10:
            if 10 <= openCard.num or openCard.num == 1:
                player.double(deck.pop())
            else:
                player.hit(deck.pop())
        elif player.score == 11:
            player.double(deck.pop())
        elif player.score == 12:
            if (4 <= openCard.num and 6 <= openCard.num):
                player.hit(deck.pop())
            else:
                break
        elif 13 <= player.score <= 14:
            if (player.softFlg == True and 5 <= dealer.score <= 6):
                player.double(deck.pop())
            elif (player.softFlg == True or 7 <= dealer.score):
                player.hit(deck.pop())
            else:
                break
        elif 15 <= player.score <= 16:
            if (player.softFlg == True and 4 <= dealer.score <= 6):
                player.double(deck.pop())
            elif (player.softFlg == True or 7 <= dealer.score):
                player.hit(deck.pop())
            else:
                break
        elif player.score == 17:
            if (player.softFlg == True and 3 <= dealer.score <= 6):
                player.double(deck.pop())
            elif (player.softFlg == True or 7 <= dealer.score):
                player.hit(deck.pop())
            else:
                break
        elif player.score == 17:
            if (player.softFlg == True and 3 <= dealer.score <= 6):
                player.double(deck.pop())
            elif (player.softFlg == True or 9 <= dealer.score):
                player.hit(deck.pop())
            else:
                break
        else:
            break
        
    # ディーラーは17未満ならヒットし続ける
    while dealer.score < 17:
        dealer.hit(deck.pop())
    player.say()
    dealer.say()

def deal():
    """
    決着
    """

    # ベット数
    bet = 0.25
    # トゥルーカウントが基準値以上なら
    if deck.trueCount() > -0.02 and deck.trueCount() != 0:
        bet = 300

    # doubleFlag = Trueなら掛け金2倍
    if (player.doubleFlag == True):
        bet *= 2

    if player.score > 21: # Player Busted!
        # print(player.name + " Lose...")
        player.fund -= bet
        player.looseCount += 1
    elif player.score == dealer.score:
        # print("Draw!")
        player.drawCount += 1
    elif player.score == 21:
        # print(player.name + "BJ!")
        player.fund += bet * 1.5
        player.winCount += 1
    elif (dealer.score > 21 or player.score > dealer.score):
        # print(player.name + " Win!")
        player.fund += bet
        player.winCount += 1
    else:
        # print(player.name + " Lose...")
        player.fund -= bet
        player.looseCount += 1
    # スコアリセット
    player.__init__()
    dealer.__init__()
    # カードを初期化
    if len(deck) < 102:
        deck.__init__()

class DeckList(list):
    """
    デッキのリスト（8デック対応）
    """

    def __init__(self, num = 8):
        """
        初期化

        Paramters
        ---------
        num : int
            デッキの総数
        """
        for i in range(num):
            self.extend(Deck())
        self.count = -(num * 2)

    def pop(self):
        """
        デッキからカードを1枚引く
        pop()のオーバーライド
        """
        card = super().pop()
        # ハイローシステム
        # if 2 <= card.num <= 6:
        #     self.count += 1
        # elif 7 <= card.num <= 9:
        #     pass
        # else:
        #     self.count -= 1

        # KOシステム
        # if 2 <= card.num <= 7:
        #     self.count += 1
        # elif 8 <= card.num <= 9:
        #     pass
        # else:
        #     self.count -= 1

        # ZEN
        if card.num == 1 or 10 <= card.num:
            self.count -= 2
        elif 8 <= card.num <= 9:
            pass
        elif 2 <= card.num <= 3 or card.num == 7:
            self.count += 1
        else:
            self.count += 2

        return card
    
    def trueCount(self):
        """
        トゥルーカウントの計算
        """
        # return self.count/len(self)
        # 2chにあった計算方法
        return self.count/(len(self))
        # return self.count/(len(self) - 0.03)

class Deck(list):
    """
    デッキクラス、リスト型を拡張
    Cardオブジェクトを52枚持つ
    """

    def __init__(self):
        for suit in ['♠', '♣', '♡', '♢']:
            for num in range(1, 14):
                self.append(Card(num, suit))
        random.shuffle(self)

class Card:
    """
    カードクラス
    """
    def __init__(self, num, suit):
        """初期化(数、マーク）"""
        self.num = num
        self.suit = suit

    def __repr__(self):
        return self.suit + str(self.num)

class Human:
    """
    人間基盤クラス
    """

    def __init__(self):
        self.hand = []
        self.name = ""
        self.score = 0
        self.softFlg = False # ソフトカードがあるかどうかのフラグ

    def draw(self, card):
        """
        draw

        Parameters
        ----------
        card : Card
            ヒットしたCardインスタンス
        """
        self.hand.append(card)
        self.calculate()

    def hit(self, card):
        """
        ヒット

        Parameters
        ----------
        card : Card
            ヒットしたCardインスタンス
        """
        self.draw(card)
        # print(self.name + " draw " + str(card))


    def calculate(self):
        """
        スコア計算
        """
        self.score = 0
        for card in self.hand:
            if card.num >= 10: # 10と絵柄の場合
                self.score += 10
            elif card.num == 1: # Aの場合
                self.softFlg = True
                self.score +=11
            else:
                self.score += card.num
        
        # 21をオーバーする場合はAを-10する
        for card in self.hand:
            if card.num == 1:
                if self.score > 21:
                    self.softFlg = False
                    self.score -= 10

    def say(self):
        """
        スコアを公開する
        """
        # print(self.name + "`s score is " + str(self.score))
        if self.score == 21:
            pass
            # print(self.name + " is BJ!")
        elif self.score > 21:
            pass
            # print(self.name + " Busted!")

    def openHand(self):
        """
        手札を公開する
        """
        # print(self.name + "`s hand are ")
        for card in self.hand:
            pass
            # print(str(card))

class Dealer(Human):
    """ディーラークラス"""
    def __init__(self):
        super().__init__()
        self.name = "Dealer"

class Player(Human):
    """プレイヤークラス"""
    fund = 1000 # 資産
    winCount = 0
    looseCount = 0
    drawCount = 0

    def __init__(self):
        super().__init__()
        self.name = "Player"
        self.doubleFlag = False
    
    def double(self, card):
        """
        ダブルダウン
        ヒット後、doubleFlagをTrueに

        Parameters
        ----------
        card : Card
            ヒットしたCardインスタンス
        """
        super().hit(card)
        self.doubleFlag = True

if __name__ == "__main__":
    main()