import requests
from datetime import date

free = '''
░░▄█████████████████▄
░▐████▀▒▒БОЛДАК▒▒▀████
░███▀▒▒▒РАЗРЕШИЛ▒▒▒▒▀██
░▐██▒▒▒▒▒АДИХНУТЬ▒▒▒▒▒██
░▐█▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███
░░█▒▄▀▀▀▀▀▄▒▒▄▀▀▀▀▀▄▒▐██
░░░▐░░░▄▄░░▌▐░░░▄▄░░▌▐██
░▄▀▌░░░▀▀░░▌▐░░░▀▀░░▌▒▀▒
░▌▒▀▄░░░░▄▀▒▒▀▄░░░▄▀▒▒▄▀
░▀▄▐▒▀▀▀▀▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒
░░░▀▌▒▄██▄▄▄▄████▄▒▒▒▒█▀
░░░░▄██████████████▒▒▐▌
░░░▀███▀▀████▀█████▀▒▌
░░░░░▌▒▒▒▄▒▒▒▄▒▒▒▒▒▒▐
░░░░░▌▒▒▒▒▀▀▀▒▒▒▒▒▒▒▐
'''

week_days = ('понедельник', 'вторник', 'среду', 'четверг', 'пятницу')

def get_current_week():
    weekUrl = 'http://api.rozklad.org.ua/v2/weeks'
    week = requests.get(weekUrl).json()['data']
    return week


def show_schedule(day: str, sch: str, hl: str, gl: str, aw: str):
    return 'Запланированные мувы на ' + day + ':\n' + '''
———————————————
{schedule}
———————————————
👺 Hotlines: 
{hotlines}
———————————————
{global_links}
———————————————
{afterword}
'''.format(schedule=sch, hotlines=hl, global_links=gl, afterword=aw)


class Schedule:
    url = 'http://api.rozklad.org.ua/v2/groups/{0}/lessons'

    def is_group_exist(self, group: str):
        return requests.get(self.url.format(group)).ok

    def getDay(self, week, day):
        schedule = ''
        r = requests.get(self.url)
        data = r.json()['data']
        for lesson in data:
            if lesson['lesson_week'] == str(week) and lesson['day_number'] == str(day):
                schedule += '\n' + lesson["time_start"][:5] + ' — <i>' + \
                            lesson["lesson_name"] + '</i> <b>\n' + \
                            lesson["lesson_type"] + "</b> — " + \
                            lesson["teacher_name"] + '\n'

        return free if (schedule == '') else schedule
