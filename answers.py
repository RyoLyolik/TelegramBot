import sys
sys.path.insert(0, '../WebServer/')
from layout import users, lvls, dbase
import json
import random
import requests
from speech import speech_it
from local_module import *

translate_token = 'trnsl.1.1.20180822T035034Z.c4e6b0734a1501db.3c10535039452db4d70963681df09234674e4b33'
all_lang = ['az', 'sq', 'am', 'en', 'ar', 'hy', 'af', 'eu', 'ba', 'be', 'bn', 'my',
            'bg', 'bs', 'cy', 'hu', 'vi', 'ht', 'gl', 'nl', 'mrj', 'el', 'ka', 'gu',
            'da', 'he', 'yi', 'id', 'ga', 'it', 'is', 'es', 'kk', 'kn', 'ca', 'ky',
            'zh', 'ko', 'xh', 'km', 'lo', 'la', 'lv', 'lt', 'lb', 'mg', 'ms', 'ml',
            'mt', 'mk', 'mi', 'mr', 'mhr', 'mn', 'de', 'ne', 'no', 'pa', 'pap', 'fa',
            'pl', 'pt', 'ro', 'ru', 'ceb', 'sr', 'si', 'sk', 'sl', 'sw', 'su', 'tg',
            'th', 'tl', 'ta', 'tt', 'te', 'tr', 'udm', 'uz', 'uk', 'ur', 'fi', 'fr',
            'hi', 'hr', 'cs', 'sv', 'gd', 'et', 'eo', 'jv', 'ja']

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
        self.status = self.user[7]
        if body.lower() == 'id':
            return 'Telegram: ' + str(self.user[6]) + '\nIn game: ' + str(self.user[0])

        elif body.lower() == 'профиль':
            user = users.get_by_tele(message.from_user.id)

            return '🆔: '+str(self.user[0])+'\n'+\
                   '❤️Жизни: '+str(self.data['player']['max_health'])+\
                   '\n❣️Регенерация: '+str(self.data['player']['regen']) + \
                   '\n💪🏻Сила: ' + str(self.data['player']['power'])+\
                   '\n💰Деньги: '+str(self.split_it(self.data['player']['money']))+'$'+\
                   '\n⭐Статус: ' + self.status

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
            return '🙎🏻‍♂️️Профиль\n💸Баланс\n🎰Казино\n🏴󠁧󠁢󠁥󠁮󠁧󠁿Переведи <с> <на> <текст>\n🖊Граф <список>/рандом\n🎤Скажи <слова>\n\nVersion 0.05'

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
            return 'Пока нельзя это улучшать'

        elif body.lower().split()[:1] == ['переведи']:

            eng_text = body.split()[1:]
            langs = [eng_text[0], eng_text[1]]
            eng_text = body.split()[3:]

            eng_text = ' '.join(eng_text)
            if langs[0] in all_lang and langs[1] in all_lang:
                url_trans = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
                trans_option = {'key': translate_token, 'lang': langs[0] + "-" + langs[1], 'text': eng_text}
                # trans_option = {'key': token, 'lang': "en-ru", 'text': eng_text}
                webRequest = requests.get(url_trans, params=trans_option)
                rus_text = webRequest.text
                srez = 32 + len(langs[0]) + len(langs[1])
                rus_text = rus_text[srez:(len(rus_text) - 3)]

                return rus_text + '\n\nПереведено сервисом «Яндекс.Переводчик»\nhttp://translate.yandex.ru/'

        elif body.lower() == 'языки':
            return '''азербайджанский	az	\nмалаялам	ml\n\
                    албанский	sq	\nмальтийский	mt\n\
                    амхарский	am	\nмакедонский	mk\n\
                    английский	en	\nмаори	mi\n\
                    арабский	ar	\nмаратхи	mr\n\
                    армянский	hy	\nмарийский	mhr\n\
                    африкаанс	af	\nмонгольский	mn\n\
                    баскский	eu	\nнемецкий	de\n\
                    башкирский	ba	\nнепальский	ne\n\
                    белорусский	be	\nнорвежский	no\n\
                    бенгальский	bn	\nпанджаби	pa\n\
                    бирманский	my	\nпапьяменто	pap\n\
                    болгарский	bg	\nперсидский	fa\n\
                    боснийский	bs	\nпольский	pl\n\
                    валлийский	cy	\nпортугальский	pt\n\
                    венгерский	hu	\nрумынский	ro\n\
                    вьетнамский	vi	\nрусский	ru\n\
                    гаитянский (креольский)	ht	\nсебуанский	ceb\n\
                    галисийский	gl	\nсербский	sr\n\
                    голландский	nl	\nсингальский	si\n\
                    горномарийский	\nmrj	словацкий	sk\n\
                    греческий	el	\nсловенский	sl\n\
                    грузинский	ka	\nсуахили	sw\n\
                    гуджарати	gu	\nсунданский	su\n\
                    датский	da	\nтаджикский	tg\n\
                    иврит	he	\nтайский	th\n\
                    идиш	yi	\nтагальский	tl\n\
                    индонезийский	id	\nтамильский	ta\n\
                    ирландский	ga	\nтатарский	tt\n\
                    итальянский	it	\nтелугу	te\n\
                    исландский	is	\nтурецкий	tr\n\
                    испанский	es	\nудмуртский	udm\n\
                    казахский	kk	\nузбекский	uz\n\
                    каннада	kn	\nукраинский	uk\n\
                    каталанский	ca	\nурду	ur\n\
                    киргизский	ky	\nфинский	fi\n\
                    китайский	zh	\nфранцузский	fr\n\
                    корейский	ko	\nхинди	hi\n\
                    коса	xh	\nхорватский	hr\n\
                    кхмерский	km	\nчешский	cs\n\
                    лаосский	lo	\nшведский	sv\n\
                    латынь	la	\nшотландский	gd\n\
                    латышский	lv	\nэстонский	et\n\
                    литовский	lt	\nэсперанто	eo\n\
                    люксембургский	lb	\nяванский	jv\n\
                    малагасийский	mg	\nяпонский	ja\n\
                    малайский	ms'''
        elif body.lower().split()[0] == 'скажи':
            speech_it(' '.join(body.lower().split()[1:]))
            return "file audio"

        elif body.lower().split()[0] == 'граф':
            if body.lower().split()[1] == 'рандом':
                nums = random.choice(range(1, 15))
                points = [i for i in range(nums)]
                comps = random.choice(range(nums, nums + 5))
                cord = [list(set([random.choice(points) for i in range(random.choice(range(1, 5)))]))
                        for i in range(nums)]
            else:
                cord = json.loads(body.lower().split()[1:])
            graph(cord)
            return 'file image|'+str(cord)

        if self.status == 'Admin':
            if body.lower().split()[0] == 'получить':
                if body.lower().split()[1].isdigit:
                    self.data['player']['money'] += int(body.lower().split()[1])
                    return 'Готово. \nБаланс:💰'+self.split_it(self.data['player']['money'])+'$'


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