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
lesson_numbers = {
    '08:30':  '1️⃣',
    '10:25':  '2️⃣',
    '12:20':  '3️⃣',
    '14:15':  '4️⃣',
    '16:10':  '5️⃣'
}



def get_current_week():
    weekUrl = 'http://api.rozklad.org.ua/v2/weeks'
    week = requests.get(weekUrl).json()['data']
    return week


def get_current_day():
    return date.today().weekday()


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
    url_for_teachers = 'http://api.rozklad.org.ua/v2/teachers/{0}/lessons'

    def is_group_exist(self, group: str):
        return requests.get(self.url.format(group)).ok

    def get_day(self, week, day):
        print('ga')
        schedule = ''
        r = requests.get(self.url)
        data = r.json()['data']
        for lesson in data:
            if lesson['lesson_week'] == str(week) and lesson['day_number'] == str(day):
                lessonStart = lesson["time_start"][:5]
                schedule += '\n' + str(lesson_numbers.get(lessonStart)) + ' ' + lessonStart + ' — <i>' + \
                            lesson["lesson_name"] + '</i> <b>\n' + \
                            lesson["lesson_type"] + "</b> — " + \
                            lesson["teacher_name"] + '\n'

        return free if (schedule == '') else schedule

    def get_day_for_teacher(self, week, day):
        schedule = ''
        r = requests.get(self.url_for_teachers)
        data = r.json()['data']
        for lesson in data:
            if lesson['lesson_week'] == str(week) and lesson['day_number'] == str(day):
                lessonStart = lesson["time_start"][:5]
                schedule += '\n' + str(lesson_numbers.get(lessonStart)) + ' ' + lessonStart + ' — <i>' + \
                            lesson["lesson_name"] + '</i> \n<b>' + \
                            lesson["lesson_type"] + "</b> — " + \
                            lesson["teacher_name"] + '\n'

                group_list = []
                for group in lesson['groups']:
                    group_list.append(group['group_full_name'])

                schedule += 'Груп'+('а: ' if len(group_list) == 1 else 'и: ') + ', '.join(group_list)

        return free if (schedule == '') else schedule
