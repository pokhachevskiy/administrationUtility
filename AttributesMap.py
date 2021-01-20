import json


class AttributesMap:
    def __init__(self, path):
        attributes_file = open(path, 'r')
        amap = json.load(attributes_file)
        self.amap = amap
        attributes_file.close()
        self.attributes = {
            'Разрешена аутентификация в АМДЗ': {'boolean': True, 'complex': False, 'name': 'amdzLoginEnabled', 'value': amap['amdzLoginEnabled']},
            'Имя пользователя': {'boolean': False, 'complex': False, 'name': 'amdzUserName', 'value': amap['amdzUserName']},
            'Группа': {'boolean': False, 'complex': False, 'name': 'amdzGroupName', 'value': amap['amdzGroupName']},
            'TM-идентификатор': {'boolean': False, 'complex': True, 'name': 'amdzTmid', 'value': amap['amdzTmid']},
            'Свертка TM-идентификатора и пароля': {'boolean': False, 'complex': False, 'name': 'amdzXid', 'value': amap['amdzXid']},
            'Открытый ключ': {'boolean': False, 'complex': False, 'name': 'amdzAuthData', 'value': amap['amdzAuthData']},
            'Последний день смены пароля': {'boolean': False, 'complex': True, 'name': 'amdzPasswordExpirationDate', 'value': amap['amdzPasswordExpirationDate']},
            'Количество попыток для изменения пароля': {'boolean': False, 'complex': True, 'name': 'amdzPasswordChangeRetriesLeft', 'value': amap['amdzPasswordChangeRetriesLeft']},
            'Привилегии администратора': {'boolean': False, 'complex': True, 'name': 'amdzAdminAttrs', 'value': amap['amdzAdminAttrs']},
            'Суперпользователь': {'boolean': True, 'complex': False, 'name': 'amdzSupervisor', 'value': amap['amdzSupervisor']},
            'Запись заблокирована': {'boolean': True, 'complex': False, 'name': 'amdzBlocked', 'value': amap['amdzBlocked']},
            'Флаг группы': {'boolean': False, 'complex': True, 'name': 'amdzGroupFlag', 'value': amap['amdzGroupFlag']},
            'Результаты процедуры ИА': {'boolean': False, 'complex': True, 'name': 'amdzIaResults', 'value': amap['amdzIaResults']},
            'Параметры пароля': {'boolean': False, 'complex': True, 'name': 'amdzPasswordParams', 'value': amap['amdzPasswordParams']},
            'Ограничения на вход в систему по времени': {'boolean': False, 'complex': True, 'name': 'amdzWorkingHours', 'value': amap['amdzWorkingHours']},
            'Количество неудачных попыток доступа': {'boolean': False, 'complex': True, 'name': 'amdzMaxAuthFails', 'value': amap['amdzMaxAuthFails']},
            'Дата начала действия учетной записи': {'boolean': False, 'complex': True, 'name': 'amdzActiveAfter', 'value': amap['amdzActiveAfter']},
            'Дата конца действия учетной записи': {'boolean': False, 'complex': True, 'name': 'amdzActiveBefore', 'value': amap['amdzActiveBefore']},
            'Имитовставка': {'boolean': False, 'complex': True, 'name': 'amdzMac', 'value': amap['amdzMac']},
        }
