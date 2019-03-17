import sys
sys.path.insert(0, '../WebServer/')
from layout import users, lvls, dbase
import json
import random

class Answers:
    def __init__(self):
        pass

    def get_answer(self, body, message):
        user_id = message.from_user.id
        self.user = users.get_by_tele(user_id)
        file = open('../WebServer/databases/player/set_' + str(self.user[0]) + '.json', mode='r')
        self.data = file.read()
        self.data = json.loads(self.data)
        file.close()
        if body.lower() == 'id':
            return 'Telegram: ' + str(self.user[-1]) + '\nIn game: ' + str(self.user[0])

        elif body.lower() == 'профиль':
            user = users.get_by_tele(message.from_user.id)

            return '🆔: '+str(self.user[0])+'\n'+'❤️Жизни: '+str(self.data['player']['max_health'])+'\n❣️Регенерация: '+str(self.data['player']['regen']) + '\n💪🏻Сила: ' + str(self.data['player']['power'])+'\n💰Деньги: '+str(self.split_it(self.data['player']['money']))+'$'

        elif body.lower().split()[0] == 'казино':
            body = body.lower().split()
            money = self.data['player']['money']
            bet = body[1]
            if bet == 'все' or bet == 'всё':
                bet = int(money)
            elif bet.isdigit() is False:
                return None
            bet = int(bet)
            if bet > money:
                bet = int(money)
            money -= int(bet)
            mult = random.random()
            if bet < 0:
                return 'Минимальная ставка 1$'
            if mult < 0.05:
                b = 0
                bet *= 0

            elif mult < 0.15:
                b = 0.25
                bet *= 0.25

            elif mult < 0.25:
                b = 0.5
                bet *= 0.5

            elif mult < 0.5:
                b = 0.75
                bet *= 0.75

            elif mult < 0.65:
                b = 1.5
                bet*= 1.5

            elif mult < 0.8:
                b = 2
                bet *= 2

            elif mult < 0.9:
                b = 5
                bet*=5

            elif mult <= 1 and mult > 0.95:
                b = 100
                bet *= 100
            else:
                b = random.choice((0.5,1,2))
            money += bet
            self.data['player']['money'] = money
            return 'Тебе попалось х'+str(b)+'\n💵Денег: '+str(self.split_it(int(money)))+'$'

        elif body.lower() == 'баланс':
            return '💵На счете: '+str(self.split_it(self.data['player']['money']))+'$'

        elif body.lower() == 'помощь':
            return '🙎🏻‍♂️️Профиль\n💸Баланс\n🎰Казино'

        elif body.lower().split()[0] == 'улучшить':
            if body.lower().split()[1] == 'себя':
                if self.data['player']['money'] >= self.data['player']['upgrade_cost']:
                    self.data['player']['money'] -= self.data['player']['upgrade_cost']
                    self.data['player']['power'] = int(round((self.data['player']['power']+1)*1.03,0))
                    self.data['player']['upgrade_cost'] = int(round(((self.data['player']['upgrade_cost']) * 1.06), 0))
                    self.data['player']['max_health'] = int(round(((self.data['player']['max_health'])*1.04),0))
                    self.data['player']['regen'] = round((self.data['player']['regen']+1) * 1.04, 5)
                    return 'Готово. Теперь: \n❤️Жизни: '+str(self.data['player']['max_health'])+'\n❣️Регенерация: '+str(self.data['player']['regen']) + '\n💪🏻Сила: ' + str(self.data['player']['power'])+'\n💰Деньги: '+str(self.split_it(self.data['player']['money']))+'$'
                return 'Недостаточно денег'
    def save(self):
        self.data['player']['money'] = int(round(self.data['player']['money'], 0))
        file = open('../WebServer/databases/player/set_' + str(self.user[0]) + '.json', mode='w')
        json.dump(self.data, file)
        file.close()

    def split_it(self, n):
        n = str(n)
        n = n[::-1]
        temp = ''
        for i in range(len(n)):
            if i%3 == 0 and i != 0:
                temp+='.'
            temp += n[i]
        return temp[::-1]