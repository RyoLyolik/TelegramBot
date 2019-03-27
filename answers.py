import sys
import json
import random
import requests
from local_module import *
import inspect
import wolframalpha
sys.path.insert(0, '../WebServer/')
from layout import users, lvls, dbase


client = wolframalpha.Client('APQHJJ-U3R79WKWHU')

translate_token = 'trnsl.1.1.20180822T035034Z.c4e6b0734a1501db.3c10535039452db4d70963681df09234674e4b33'
all_lang = ['az', 'sq', 'am', 'en', 'ar', 'hy', 'af', 'eu', 'ba', 'be', 'bn', 'my',
            'bg', 'bs', 'cy', 'hu', 'vi', 'ht', 'gl', 'nl', 'mrj', 'el', 'ka', 'gu',
            'da', 'he', 'yi', 'id', 'ga', 'it', 'is', 'es', 'kk', 'kn', 'ca', 'ky',
            'zh', 'ko', 'xh', 'km', 'lo', 'la', 'lv', 'lt', 'lb', 'mg', 'ms', 'ml',
            'mt', 'mk', 'mi', 'mr', 'mhr', 'mn', 'de', 'ne', 'no', 'pa', 'pap', 'fa',
            'pl', 'pt', 'ro', 'ru', 'ceb', 'sr', 'si', 'sk', 'sl', 'sw', 'su', 'tg',
            'th', 'tl', 'ta', 'tt', 'te', 'tr', 'udm', 'uz', 'uk', 'ur', 'fi', 'fr',
            'hi', 'hr', 'cs', 'sv', 'gd', 'et', 'eo', 'jv', 'ja']

items = {
    'Hand':None,
    'Usual_Sword': 'textures/items/usual_sword.png',
    'Secret_Sword': 'textures/items/secret_sword.png'
}

shop = {
    'рейтинг': 1000000
}

status_system = {
    'user': 0,
    'moder': 1,
    'admin': 2
}

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
        self.file_ban = open('black_list.txt', mode='r')
        self.black_list = self.file_ban.read().split('\n')
        self.black_list[0] = 'ID|BY|REASON'
        self.file_ban.close()
        if body.lower() == 'id':
            return 'Telegram: ' + str(self.user[6]) + '\nIn game: ' + str(self.user[0])

        elif body.lower().split()[0] == 'профиль':
            all_banned = [i.split('|')[0] for i in self.black_list]
            try:
                if (self.status == 'admin' or self.status == 'moder' or self.user[6] == 454666989) and len(body.split()) > 1:
                    user = users.get(body.lower().split()[1])
                    us_id = user[0]
                    file = open('../WebServer/databases/player/set_' + str(user[0]) + '.json', mode='r')
                    data = file.read()
                    file.close()
                    data = json.loads(data)
                    return '👤️️️️Имя: ' + str(user[1]) + \
                           '\n🆔: ' + str(user[0]) + \
                           '\n📧E-mail: ' + str(user[4]) + \
                           '\n💰Деньги: ' + self.split_it(data['player']['money']) + '$' + \
                           '\n👑Рейтинг: ' + self.split_it(str(data['player']['rating'])) + \
                           '\n❤️Жизни: ' + str(self.split_it(data['player']['max_health'])) + \
                           '\n❣️Регенерация: ' + str(self.split_it(data['player']['regen'])) + \
                           '\n💪🏻Сила: ' + str(self.split_it(data['player']['power'])) + \
                           '\n🆙Стоимсоть улучшения: ' + str(
                        self.split_it(data['player']['upgrade_cost'])) + '$' + \
                           '\n⭐Статус: ' + user[7] + \
                           '\n🚫Banned: ' + str(str(user[0]) in all_banned)
            except TypeError:
                return '❌ ID does not exist. \n\nLine  ' + str(inspect.currentframe().f_lineno)

            return '🙎🏻‍♂️️Имя: ' + str(self.user[1]) + \
                   '\n🆔: ' + str(self.user[0]) + \
                   '\n📧E-mail: ' + str(self.user[4]) + \
                   '\n💰Деньги: ' + str(self.split_it(self.data['player']['money'])) + '$' + \
                   '\n👑Рейтинг: ' + self.split_it(self.data['player']['rating']) + \
                   '\n❤️Жизни: ' + str(self.split_it(self.data['player']['max_health'])) + \
                   '\n❣️Регенерация: ' + str(self.split_it(self.data['player']['regen'])) + \
                   '\n💪🏻Сила: ' + str(self.split_it(self.data['player']['power'])) + \
                   '\n🆙Стоимсоть улучшения: ' + str(self.split_it(self.data['player']['upgrade_cost'])) + '$' + \
                   '\n⭐Статус: ' + self.status + \
                   '\n🚫Banned: ' + str(str(self.user[0]) in all_banned)

        elif body.lower().split()[0] == 'казино' and len(body.split()) > 1:
            body = body.lower().split()
            money = self.data['player']['money']
            bet = body[1]
            if bet == 'все' or bet == 'всё':
                bet = int(money)
            elif bet.isdigit() is False:
                return '❌ Bet must be integer.'
            bet = int(bet)
            if bet > money:
                return '😔 Недостаточно денег'
            money -= int(bet)
            mult = random.random()
            if bet < 0:
                return 'Минимальная ставка 1$'
            if mult < .050:
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
                bet *= 1.5

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
            self.data['player']['money'] = int(round(money,0))
            return 'Тебе попалось х'+str(b)+'\n💳Денег: '+str(self.split_it(self.data['player']['money']))+'$'

        elif body.lower() == 'баланс':
            return '💵На счете: '+str(self.split_it(self.data['player']['money']))+'$'

        elif body.lower() == 'помощь':
            ret = '👤️️Профиль\n💳Баланс\n🎰Казиноn\n🗃Инвентарь\n⬆️Улучшить себя <к-во раз>\n🛒Магазин\n💎Купить <вещь> <кол-во>󠁧󠁢󠁥󠁮󠁧󠁿\n🔼Топ\n\n🌍Переведи <с> <на> <текст>\n📄Граф <список>/рандом\n🎧Скажи <слова>\n📝Реши <пример>\n🧮WA <команда> (wolframalpha)\n\nЗаново <пароль>\nVersion 0.2'
            if self.status == 'admin' or self.user[6] == 454666989:
                return ret + '\n\n👽Admin\n💰Получить <сумма>\n🖊edit <user_id>/me:\n        ⭐status <val>\n        👑rating <val>\n        🙎🏻‍♂️name <val>\n        💲money <val>\n        ❤️health <val>\n        ❣️regen <val>\n        💪🏻power <val>\n        🎚level <val>\n        🆙upgrade_cost <val>\n⛔Ban <id> <reason>\n✅Unban <id>\n\nAdmin version 0.0.4'
            elif self.status == 'moder' or self.user[6] == 454666989:
                return ret + '\n\n📱Moder\n💰Получить <сумма>\n🖊edit me:\n        ⭐status <val>\n        👑rating <val>\n        🙎🏻‍♂️name <val>\n        💲money <val>\n        ❤️health <val>\n        ❣️regen <val>\n        💪🏻power <val>\n        🎚level <val>\n        🆙upgrade_cost <val>\n⛔Ban <id> <reason>\n✅Unban <id>\n\nModer version 0.0.3'
            return ret
        elif body.lower().split()[0] == 'улучшить':
            if body.lower().split()[1] == 'себя':
                x = 1
                if len(body.lower().split()) >= 3:
                    if body.lower().split()[2].isdigit:
                        x = int(body.lower().split()[2])

                if self.data['player']['money'] >= self.data['player']['upgrade_cost'] * x:
                    self.data['player']['money'] -= self.data['player']['upgrade_cost'] * x
                    self.data['player']['power'] = int(round((self.data['player']['power'] + 1) * 1.03, 0)) * x
                    self.data['player']['upgrade_cost'] = int(
                        round(((self.data['player']['upgrade_cost']) * 1.06 + 1), 0)) * x
                    self.data['player']['max_health'] = int(round(((self.data['player']['max_health']) * 1.04), 0)) * x
                    self.data['player']['regen'] = round((self.data['player']['regen'] + 1) * 1.01, 0) * x
                    return 'Готово. Теперь: \n❤️Жизни: ' + str(
                        self.split_it(self.data['player']['max_health'])) + '\n❣️Регенерация: ' + str(
                        self.split_it(self.data['player']['regen'])) + '\n💪🏻Сила: ' + str(
                        self.split_it(self.data['player']['power'])) + '\n💰Деньги: ' + str(
                        self.split_it(self.data['player']['money'])) + '$'
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

        elif body.lower().split()[0] == 'скажи' or body.lower().split()[0] == 'ттс' or body.lower().split()[0] == 'tts':
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
                cord = json.loads(' '.join(body.lower().split()[1:]))
            graph(cord)
            return 'file image|drew.png|Вот граф '+str(cord)

        elif body.lower().split()[0] == 'инвентарь':
            invsee = [[],[],[],[],[],[],[],[]]
            cnt = 0
            for i in self.data['inventory']:
                invsee[cnt % 8].append(items[self.data['inventory'][i]['type']])
                cnt += 1
            invsee[cnt % 8].append(items[self.data['inventory'][i]['type']])
            draw_inventory(invsee)

            return 'file image|inventory.png|🗃Ваш инвентарь:'

        elif body.lower() == 'магазин':
            return '👑Рейтинг: 1шт = 1.000.000$'

        elif body.lower().split()[0] == 'купить':
            if body.lower().split()[1] in shop and body.lower().split()[2].isdigit():
                if body.lower().split()[1] == 'рейтинг':
                    if int(body.lower().split()[2]) * shop[body.lower().split()[1]] <= self.data['player']['money']:
                        self.data['player']['money'] -= shop[body.lower().split()[1]] * int(
                            body.lower().split()[2])
                        self.data['player']['rating'] += int(body.lower().split()[2])
                        return 'Готово. Теперь у тебя 👑' + self.split_it(
                            self.data['player']['rating']) + ' рейтинга.\nДенег 💳' + str(
                            self.split_it(self.data['player']['money'])) + '$'
                    return '😔Недостаточно денег.'
                else:
                    return 'Пока не доступно'

            return '❌ Wrong value. Third argument must be integer. \n\nLine  ' + str(inspect.currentframe().f_lineno) if self.status == 'admin' or self.status == 'moder' or self.user[6] == 454666989 else '❌ Wrong value. Third argument must be integer.'

        elif body.lower().split()[0] == 'топ':
            all_users = users.get_all()
            top = []
            banned_ids = [i.split('|')[0] for i in self.black_list]
            for user in all_users:
                if user[7] == 'user' and user[6] != 454666989 and str(user[0]) not in banned_ids:
                    file = file_to_change = open('../WebServer/databases/player/set_' + str(user[0]) + '.json', mode='r')
                    top.append([json.loads(file.read())['player']['rating'], user[1], user[0]])
                    file.close()
            if len(top) != 0:
                top.sort(key=lambda x:x[0])
                top.reverse()
                top = top[:5]
                for i in range(len(top)):
                    top[i] = str(i+1)+'. ID: ' + str(top[i][2])+'   '+str(top[i][1])+' 👑'+str(self.split_it(top[i][0]))
            return 'Топ игроков:\n'+'\n'.join(top)
        elif body.lower().split()[0] == 'реши':
            try:
                return 'Выражение равно:\n'+str(eval(''.join(body.lower().split()[1:])))+'\nИли\n' + self.split_it((eval(''.join(body.lower().split()[1:]))))
            except NameError:
                return '❌ Wrong value. \n\nLine  ' + str(inspect.currentframe().f_lineno) if self.status == 'admin' or self.status == 'moder' or self.user[6] == 454666989 else '❌ Wrong value.'
        elif body.lower().split()[0] == 'заново':
            if len(body.lower().split()) > 1:
                if body.lower().split()[1] == self.user[2]:
                    file = open('../WebServer/databases/default.json', mode='r')
                    default_data = file.read()
                    file.close()
                    default_data = json.loads(default_data)
                    self.data = default_data
                    return 'Вы начали заново.'

                return 'Неверный пароль.'
            return 'Вы не указали пароль'

        elif body.lower().split()[0] == 'wa' and len(body.lower().split()) >= 3:
            res = client.query(' '.join(body.split()[1:]))
            if res['@error'] == 'false' and res['@success'] == 'true':
                if body.lower().split()[1] == 'solve':
                    pre = [i for i in res.results]
                    pre = pre[0]['subpod']
                    re_val = ''
                    if isinstance(pre, list):
                        for i in pre:
                            re_val += i['img']['@title'] + '\n'
                    else:
                        re_val = pre['img']['@title']

                    return str(re_val)

                elif body.lower().split()[1] == 'plot':
                    pre = res['pod'][1]['subpod']
                    if isinstance(pre, list):
                        re_val = pre[0]['img']['@src']
                    else:
                        re_val = pre['img']['@src']

                    return str(re_val)

                else:
                    try:
                        return next(res.results).text
                    except Exception:
                        return '❌ Error.\n\nLine ' + str(inspect.currentframe().f_lineno)

        else:
            if self.status.lower() == 'admin' or self.user[6] == 454666989:
                try:
                    all_users = users.get_all()
                    all_ids = [str(user[0]) for user in all_users]
                    if body.lower().split()[0] == 'edit' and len(body.split()) >= 4 and body.lower().split()[1] != 'me':
                        player_id = int(body.lower().split()[1])
                        if body.lower().split()[2] == 'status' and (player_id != self.user[7] or self.user[7] == 454666989):
                            if body.lower().split()[3] not in 'moderadminuser':
                                raise ValueError
                            if body.lower().split()[1] in all_ids:
                                users.update_status(player_id, body.lower().split()[3])
                                return '🙂Готово. Теперь игрок ' + str(users.get(player_id)[1]) + ' (' + str(
                                    player_id) + ') имеет статус ' + body.lower().split()[3]
                            return '❌ ID does not exist.'

                        elif body.lower().split()[2] == 'name':
                            users.update_name(player_id, ' '.join(body.split()[3:]))
                            return '🙂Готово. Теперь игрок ' + str(player_id) + '(' + str(
                                users.get(player_id)[1]) + ') имеет имя ' + ' '.join(body.split()[3:])
                        else:
                            file_to_change = open('../WebServer/databases/player/set_' + str(
                                body.lower().split()[1]) + '.json', mode='r')
                            data_player = file_to_change.read()
                            file_to_change.close()
                            data_player = json.loads(data_player)

                            data_player['player'][body.lower().split()[2]] = int(body.split()[3])

                            file_to_change = open('../WebServer/databases/player/set_' + str(
                                body.lower().split()[1]) + '.json', mode='w')

                            json.dump(data_player, file_to_change)
                            file_to_change.close()
                            if int(body.lower().split()[1]) == self.user[0]:
                                self.data = data_player
                            return '🙂Готово. Теперь игрок '  + str(users.get(player_id)[1]) + ' (' + str(player_id) + ') имеет ' + body.lower().split()[2] + ' ' + str(self.split_it(body.split()[3]))

                except ValueError:
                    return '❌ Wrong value. \n\n1.Status must be only admin/user/moder. \n2.Money/regen/power/upgrade_cost/level/max_health must be integer. \n\nLine ' + str(inspect.currentframe().f_lineno)

                except FileNotFoundError:
                    return '❌ ID does not exist. \n\nLine  ' + str(inspect.currentframe().f_lineno)

            if self.status.lower() == 'moder' or self.status.lower() == 'admin' or self.user[6] == 454666989:
                try:
                    if body.lower().split()[0] == 'получить':
                        if body.lower().split()[1].isdigit:
                            self.data['player']['money'] += int(body.lower().split()[1])
                            return '🙂Готово. \nБаланс: 💰' + self.split_it(
                                self.data['player']['money']) + '$'

                        return '❌ Wrong value. \n\nLine  ' + str(inspect.currentframe().f_lineno)

                    elif body.lower().split()[0] == 'edit' and len(body.split()) >= 4 and body.lower().split()[
                        1] == 'me':
                        player_id = self.user[0]
                        if body.lower().split()[2] == 'status' and self.user[6] == 454666989:
                            possible_status = 'adminmoderuser' if self.status.lower() == 'admin' or self.user[6] == 454666989 else 'moderuser'
                            if body.lower().split()[3] not in possible_status:
                                raise ValueError
                            users.update_status(player_id, body.lower().split()[3])
                            return 'Готово. Теперь ты имеешь статус ' + body.lower().split()[3]

                        elif body.lower().split()[2] == 'name' and len(body.split()) >= 4:
                            users.update_name(player_id, ' '.join(body.split()[3:]))
                            return 'Готово. Теперь игрок имеешь имя ' + ' '.join(body.split()[3:])
                        elif len(body.split()) >= 4:
                            file_to_change = open('../WebServer/databases/player/set_' + str(
                                player_id) + '.json', mode='r')
                            data_player = file_to_change.read()
                            file_to_change.close()
                            data_player = json.loads(data_player)
                            data_player['player'][body.lower().split()[2]] = int(body.split()[3])

                            file_to_change = open('../WebServer/databases/player/set_' + str(
                                body.lower().split()[1]) + '.json', mode='w')

                            json.dump(data_player, file_to_change)
                            file_to_change.close()
                            if int(player_id) == self.user[0]:
                                self.data = data_player
                            return '🙂Готово. Теперь ты имеешь ' + body.lower().split()[2] + ' ' + str(self.split_it(body.split()[3]))
                except ValueError:
                    return '❌ Wrong value. \n\nLine  ' + str(inspect.currentframe().f_lineno)

                if body.lower().split()[0] == 'ban' and len(body.split()) >= 3:
                    all_users = users.get_all()
                    all_ids = [str(user[0]) for user in all_users]
                    all_banned = [i.split('|')[0] for i in self.black_list]
                    if body.lower().split()[1] != str(self.user[0]):
                        if body.lower().split()[1] in all_ids and body.lower().split()[1] not in all_banned:
                            will_ban_user = users.get(body.lower().split()[1])
                            if len(body.split()) >= 3:
                                if (status_system[self.status] < status_system[will_ban_user[7]] and will_ban_user[
                                    6] != 454666989) or self.user[6] == 454666989:
                                    if '|' not in ' '.join(body.split()[2:]):
                                        self.black_list.append(
                                            body.lower().split()[1] + '|' + str(self.user[0]) + '|' + ' '.join(
                                                body.split()[2:]))
                                        return body.lower().split()[1] + ' (' + users.get(body.lower().split()[1])[
                                            1] + ') was banned. Reason: ' + ' '.join(body.split()[2:])
                                    return '❌ Wrong symbol "|".'
                                return '❌ You tries to ban user that above you by status.'
                            return '❌ No reason.'
                        elif body.lower().split()[1] in all_banned:
                            return '❌ This player is already banned.'
                        return '❌ ID does not exists.'
                    return '❌ You wants to ban yourself.'
                elif body.lower().split()[0] == 'ban' and len(body.lower().split()) < 3:
                    return '❌ No reason.'

                elif body.lower().split()[0] == 'unban':
                    all_users = users.get_all()
                    all_banned = [i.split('|')[0] for i in self.black_list]
                    if body.lower().split()[1] in all_banned:
                        self.black_list.pop(all_banned.index(body.lower().split()[1]))
                        return body.lower().split()[1] + ' (' + \
                               users.get(body.lower().split()[1])[1] + ') was unbanned successful.'
                    return '❌ ID does not banned.'

                elif body.lower().split()[0] == 'get_all' or body.lower().split()[0] == 'all':
                    all_users = users.get_all()
                    all = [str(i) + '. ID: ' + str(all_users[i][0]) + ' Name: ' + all_users[i][1] for i in
                           range(len(all_users))]
                    return '\n'.join(all)

                elif body.lower().split()[0] == 'blacklist' or body.lower().split()[0] == 'banlist':
                    return '\n'.join([' | '.join(i.split('|')) for i in self.black_list])




    def save(self):
        self.data['player']['money'] = int(round(self.data['player']['money'], 0))
        file = open('../WebServer/databases/player/set_' + str(self.user[0]) + '.json', mode='w')
        json.dump(self.data, file)
        file.close()
        file = open('black_list.txt', mode='w')
        file.writelines('\n'.join(self.black_list))
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