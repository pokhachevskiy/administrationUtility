import json


class AttributesMap:
    def __init__(self, path):
        attributes_file = open(path, 'r')
        amap = json.load(attributes_file)
        self.amap = amap
        attributes_file.close()
        self.attributes = {
            'Разрешена аутентификация в АМДЗ': {'boolean': True, 'complex': False, 'value': amap['amdzLoginEnabled']},
            'Имя пользователя': {'boolean': False, 'complex': False, 'value': amap['amdzUserName']},
            'Группа': {'boolean': False, 'complex': False, 'value': amap['amdzGroupName']},
            'TM-идентификатор': {'boolean': False, 'complex': True, 'value': amap['amdzTmid']},
            'Свертка TM-идентификатора и пароля': {'boolean': False, 'complex': False, 'value': amap['amdzXid']},
            'Открытый ключ': {'boolean': False, 'complex': False, 'value': amap['amdzAuthData']},
            'Последний день смены пароля': {'boolean': False, 'complex': False, 'value': amap['amdzPasswordExpirationDate']},
            'Количество попыток для изменения пароля': {'boolean': False, 'complex': False, 'value': amap['amdzPasswordChangeRetriesLeft']},
            'Привилегии администратора': {'boolean': False, 'complex': False, 'value': amap['amdzAdminAttrs']},
            'Флаг суперпользователя': {'boolean': False, 'complex': False, 'value': amap['amdzSupervisor']},
            'Запись заблокирована': {'boolean': False, 'complex': False, 'value': amap['amdzBlocked']},
            'Флаг группы': {'boolean': False, 'complex': False, 'value': amap['amdzGroupFlag']},
            'Результаты процедуры ИА': {'boolean': False, 'complex': False, 'value': amap['amdzIaResults']},
            'Параметры пароля': {'boolean': False, 'complex': False, 'value': amap['amdzPasswordParams']},
            'Ограничения на вход в систему по времени': {'boolean': False, 'complex': True, 'value': amap['amdzWorkingHours']},
            'Время действия пароля в днях': {'boolean': False, 'complex': False, 'value': amap['amdzLongLifeDays']},
            'Макс число идущих подряд попыток аутентификации': {'boolean': False, 'complex': False, 'value': amap['amdzMaxAuthFails']},
            'Дата начала действия учетной записи': {'boolean': False, 'complex': True, 'value': amap['amdzActiveAfter']},
            'Дата конца действия учетной записи': {'boolean': False, 'complex': True, 'value': amap['amdzActiveBefore']},
            'Имитовставка': {'boolean': False, 'complex': True, 'value': amap['amdzMac']},
        }
