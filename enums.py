class Forma22Enum:
    VALUES_MAPPING = {
        '01': 'сельскохозяйственные организации, использующие предоставленные им земли для ведения сельского '
              'хозяйства, в том числе в исследовательских и учебных целях, а также для ведения подсобного хозяйства',
        '02': 'сельскохозяйственные организации Министерства сельского хозяйства и продовольствия Республики Беларусь',
        '03': 'крестьянские (фермерские) хозяйства',
        '05': 'граждане, использующие земельные участки для строительства и (или) обслуживания жилого дома',
        '06': 'граждане, использующие земельные участки для ведения личного подсобного хозяйства',
        '07': 'граждане, использующие земельные участки для садоводства и дачного строительства',
        '08': 'граждане, использующие земельные участки для огородничества',
        '09': 'граждане, использующие земельные участки для сенокошения и выпаса сельскохозяйственных животных',
        '10': 'граждане, использующие земельные участки для иных сельскохозяйственных целей',
        '11': 'граждане, использующие земельные участки для иных несельскохозяйственных целей',
        '12': 'промышленные организации',
        '13': 'организации железнодорожного транспорта',
        '14': 'организации автомобильного транспорта',
        '15': 'организации Вооруженных Сил Республики Беларусь, воинских частей, военных учебных заведений и других '
              'войск и воинских формирований Республики Беларусь',
        '16': 'организации воинских частей, военных учебных заведений и других войск и воинских формирований '
              'иностранных государств',
        '17': 'организации связи, энергетики, строительства, торговли, образования, здравоохранения и иные '
              'землепользователи',
        '18': 'организации природоохранного, оздоровительного, рекреационного и историко - культурного назначения',
        '19': 'заповедники, национальные парки и дендрологические парки',
        '20': 'организации, ведущие лесное хозяйство',
        '21': 'организации, эксплуатирующие и обслуживающие гидротехнические и иные водохозяйственные сооружения',
        '22': 'земли, земельные участки, не предоставленные землепользователям',
        '23': 'земли общего пользования в населенных пунктах, садоводческих товариществах и дачных кооперативах, '
              'а также земельные участки, используемые гражданами',
        '24': 'иные земли общего пользования за пределами границ населенных пунктов',
    }

    @classmethod
    def get_value(cls, key):
        return cls.VALUES_MAPPING.get(key, f'Неизвестное значение {key}')

    @classmethod
    def get_keys(cls):
        return cls.VALUES_MAPPING.keys()


class SVovlechEnum:
    INFO_MAPPING = {
        1: 'подлежат включению в границы населенного пункта для его развития',
        2: 'подлежат вовлечению в сельскохозяйственный оборот',
        3: 'подлежат вовлечению в лесохозяйственный оборот',
        4: 'подлежат вовлечению для использования в иных целях',
        6: 'включены в границы населенного пункта для его развития',
        7: 'вовлечены в сельскохозяйственный оборот',
        8: 'вовлечены в лесохозяйственный оборот',
        9: 'вовлечены для использования в иных целях',
        5: 'не могут быть использованы в хозяйственной деятельности',
    }

    @classmethod
    def get_info_value(cls, key):
        return cls.INFO_MAPPING.get(key, f'Неизвестное значение {key}')

    @classmethod
    def get_info_keys(cls):
        return cls.INFO_MAPPING.keys()