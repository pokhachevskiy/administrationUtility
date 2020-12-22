import json


class AttributesMap:
    def __init__(self, path):
        attributes_file = open(path, 'r')
        attributes_map = json.load(attributes_file)
        attributes_file.close()
        self.attributes = {
            'Разрешена аутентификация в АМДЗ': {'boolean': True, 'complex': False, 'value': attributes_map['amdzLoginEnabled']},
            'Имя пользователя': {'boolean': False, 'complex': False, 'value': attributes_map['amdzUserName']},
            'Группа': {'boolean': False, 'complex': False, 'value': attributes_map['amdzGroupName']},
            'TM-идентификатор': {'boolean': False, 'complex': True, 'value': attributes_map['amdzTmid']},
            'Свертка TM-идентификатора и пароля': {'boolean': False, 'complex': False, 'value': attributes_map['amdzXid']},
            'Открытый ключ': {'boolean': False, 'complex': False, 'value': attributes_map['amdzAuthData']},
            'Последний день смены пароля': {'boolean': False, 'complex': False, 'value': attributes_map['amdzPasswordExpirationDate']},
            'Количество попыток для изменения пароля': {'boolean': False, 'complex': False, 'value': attributes_map['amdzPasswordChangeRetriesLeft']},
            'Привилегии администратора': {'boolean': False, 'complex': False, 'value': attributes_map['amdzAdminAttrs']},
            'Флаг суперпользователя': {'boolean': False, 'complex': False, 'value': attributes_map['amdzSupervisor']},
            'Запись заблокирована': {'boolean': False, 'complex': False, 'value': attributes_map['amdzBlocked']},
            'Флаг группы': {'boolean': False, 'complex': False, 'value': attributes_map['amdzGroupFlag']},
            'Результаты процедуры ИА': {'boolean': False, 'complex': False, 'value': attributes_map['amdzIaResults']},
            'Параметры пароля': {'boolean': False, 'complex': False, 'value': attributes_map['amdzPasswordParams']},
            'Ограничения на вход в систему по времени': {'boolean': False, 'complex': True, 'value': attributes_map['amdzWorkingHours']},
            'Время действия пароля в днях': {'boolean': False, 'complex': False, 'value': attributes_map['amdzLongLifeDays']},
            'Макс число идущих подряд попыток аутентификации': {'boolean': False, 'complex': False, 'value': attributes_map['amdzMaxAuthFails']},
            'Дата начала действия учетной записи': {'boolean': False, 'complex': True, 'value': attributes_map['amdzActiveAfter']},
            'Дата конца действия учетной записи': {'boolean': False, 'complex': True, 'value': attributes_map['amdzActiveBefore']},
            'Имитовставка': {'boolean': False, 'complex': True, 'value': attributes_map['amdzMac']},
        }
