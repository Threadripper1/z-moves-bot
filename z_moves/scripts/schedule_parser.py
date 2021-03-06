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

url_for_students_pattern = 'http://api.rozklad.org.ua/v2/groups/{0}/lessons'
url_for_teachers_pattern = 'http://api.rozklad.org.ua/v2/teachers/{0}/lessons'

week_days = {
    1: 'понедельник',
    2: 'вторник',
    3: 'среду',
    4: 'четверг',
    5: 'пятницу'
}
lesson_numbers = {
    '08:30': '1️⃣',
    '10:25': '2️⃣',
    '12:20': '3️⃣',
    '14:15': '4️⃣',
    '16:10': '5️⃣'
}


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
    role: str
    url: str

    @staticmethod
    def is_teacher_exist(name: str):
        url = url_for_teachers_pattern
        return requests.get(url.format(name)).ok

    @staticmethod
    def is_group_exist(group: str):
        url = url_for_students_pattern
        return requests.get(url.format(group)).ok

    def get_schedule(self, week, day):
        schedule = ''
        if self.role == 'студент':
            r = requests.get(self.url)
            data = r.json()['data']
            for lesson in data:
                if lesson['lesson_week'] == str(week) and lesson['day_number'] == str(day):
                    lessonStart = lesson["time_start"][:5]
                    schedule += '\n' + str(lesson_numbers.get(lessonStart)) + ' ' + lessonStart + ' — <i>' + \
                                lesson["lesson_name"] + '</i> <b>\n' + \
                                lesson["lesson_type"] + "</b> — " + \
                                lesson["teacher_name"] + '\n'

        elif self.role == 'преподаватель':
            r = requests.get(self.url)
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
                    schedule += 'Груп' + ('а: ' if len(group_list) == 1 else 'и: ') + ', '.join(group_list) + '\n'
        else:
            schedule = 'Не удаётся вас распознать'

        return free if (schedule == '') else schedule

    @staticmethod
    def get_teacher_name(full_name: str):
        name = full_name.split(' ')
        return name[1] + ' ' + name[2]

    def identify_as(self, role: str, id: str):
        if role == 'студент':
            self.url = url_for_students_pattern
        elif role == 'преподаватель':
            self.url = url_for_teachers_pattern
        else:
            raise AttributeError('Cannot identify your role')

        self.url = self.url.format(id)
        self.role = role
