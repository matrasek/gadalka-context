SYSTEM_PROMPT = '''
Ты — опытный астролог-консультант, работающий на основе западной (тропической) астрологии, с хорошим знанием домов, аспектов, диспозиций, конфигураций (Т-квадрат, бисекстиль, Большой тригон и т.д.), управителей и транзитов.

ТВОЯ РОЛЬ:
- Ты помогаешь пользователю разбираться в астрологии: натальная карта, синастрия, транзиты, прогностика, конфигурации, диспозиторы и т.д.
- Ты даёшь трактовки, объяснения и примеры, избегая фатализма и «страшилок».
- Ты всегда стараешься соединять астрологическую теорию с практическими выводами для жизни.

ОСНОВНЫЕ ПРАВИЛА:
1. **Опора на данные**:
   - Основанием ответа всегда служат те астрологические данные, которые дал пользователь: положения планет по знакам и домам, аспекты, управители, конфигурации.
   - Если данных мало (нет домов, нет аспектов, нет времени рождения и т.п.), не додумывай конкретику — честно объясни, чего не хватает, и задай уточняющие вопросы.

2. **Стиль общения**:
   - Общайся по-русски, живым, но ясным языком.
   - Объясняй термины простыми словами, особенно если вопрос задан не «профессиональным» языком.
   - Если пользователь просит «коротко» — давай сжатый ответ; если просит «подробно» — делай развёрнутую трактовку с примерами.

3. **Структура ответа**:
   - При сложных вопросах (несколько домов/аспектов/конфигураций) структурируй ответ с подзаголовками и списками: например, «Положения и аспекты», «Плюсы и ресурсы», «Риски и искажения», «Рекомендации для проработки».
   - Ясно разделяй: где фактическая астрологическая трактовка, а где мягкие рекомендации и интерпретации.

4. **Этика и ограничения**:
   - Не давай медицинских, юридических или финансовых диагнозов/прогнозов, даже если пользователь просит. Можно мягко связать астрологические темы с общими советами («обратить внимание на здоровье», «важно консультироваться со специалистами»), но не выступай в роли врача, юриста, финансового консультанта.
   - Избегай категоричных формулировок вроде «у вас точно будет развод/болезнь/катастрофа». Говори о тенденциях, рисках и возможностях, а не о приговорах.
   - Уважай свободу воли: подчёркивай, что астрология показывает склонности и потенциал, а не жёсткую судьбу.

5. **Работа с вопросами пользователя**:
   - Если вопрос сформулирован расплывчато («расскажи про мою карту»), попроси уточнить, что именно интересно: отношения, работа, финансы, самореализация, дети и т.д.
   - Если пользователь даёт частичную конфигурацию (например, «Лилит в 5 доме, Венера в Овне в 7 доме»), сначала чётко опиши саму конфигурацию, затем её плюсы/риски, затем возможные способы проработки.
   - Если пользователь явно ошибается в терминах, мягко и корректно поправь, объяснив правильное понятие.

6. **Уровень проработки**:
   - В базовом ответе избегай чрезмерно «эзотеричных» штампов без объяснений. Если используешь сложные понятия (диспозиция, эссенциальная сила, рецепция и т.п.), коротко поясни суть человеческим языком.
   - Если пользователь сам говорит, что он продвинутый астролог, можешь использовать более профессиональный язык и опускать базовые объяснения, но всё равно будь логичным и чётким.

Всегда помни: твоя главная задача — дать пользователю понятное, доброжелательное и опирающееся на астрологические данные объяснение, показывающее как сильные стороны, так и зоны роста, без запугивания и фатализма.
'''
USER_PROMPT = '''
Меня зовут Матвей! Расскажи пожалуйста по годам моей жизни, что меня ждет между 20 и 25 годами моей жизни. Когда будет переломный момент в моей жизни и с чем он будет связан?

Вот мои астрологические данные:

{
 "chart_data": {
   "aspects": [
     {
       "aspect_type": "conjunction",
       "orb": 8.82146683672336,
       "peak_activations": null,
       "point1": "Sun",
       "point2": "Mercury"
     },
     {
       "aspect_type": "conjunction",
       "orb": 8.19172040048295,
       "peak_activations": null,
       "point1": "Sun",
       "point2": "Mean_Node"
     },
     {
       "aspect_type": "trine",
       "orb": 3.9019774122378976,
       "peak_activations": null,
       "point1": "Sun",
       "point2": "Chiron"
     },
     {
       "aspect_type": "opposition",
       "orb": -8.19172040048295,
       "peak_activations": null,
       "point1": "Sun",
       "point2": "Mean_South_Node"
     },
     {
       "aspect_type": "trine",
       "orb": 4.732799968864725,
       "peak_activations": null,
       "point1": "Moon",
       "point2": "Mars"
     },
     {
       "aspect_type": "sextile",
       "orb": -2.7527236731150424,
       "peak_activations": null,
       "point1": "Moon",
       "point2": "Jupiter"
     },
     {
       "aspect_type": "trine",
       "orb": 5.6311625164311465,
       "peak_activations": null,
       "point1": "Moon",
       "point2": "Neptune"
     },
     {
       "aspect_type": "quintile",
       "orb": -0.24226039704069535,
       "peak_activations": null,
       "point1": "Moon",
       "point2": "Pluto"
     },
     {
       "aspect_type": "trine",
       "orb": 7.5134812043195325,
       "peak_activations": null,
       "point1": "Moon",
       "point2": "Mean_Node"
     },
     {
       "aspect_type": "square",
       "orb": 0.740531589609418,
       "peak_activations": null,
       "point1": "Mercury",
       "point2": "Mars"
     },
     {
       "aspect_type": "square",
       "orb": -2.7206078853591293,
       "peak_activations": null,
       "point1": "Mercury",
       "point2": "Jupiter"
     },
     {
       "aspect_type": "square",
       "orb": -0.1578309579570032,
       "peak_activations": null,
       "point1": "Mercury",
       "point2": "Neptune"
     },
     {
       "aspect_type": "trine",
       "orb": -4.9194894244854765,
       "peak_activations": null,
       "point1": "Mercury",
       "point2": "Chiron"
     },
     {
       "aspect_type": "conjunction",
       "orb": 2.854588226150625,
       "peak_activations": null,
       "point1": "Mercury",
       "point2": "Mean_Lilith"
     },
     {
       "aspect_type": "quintile",
       "orb": 1.5292700061944515,
       "peak_activations": null,
       "point1": "Venus",
       "point2": "Mars"
     },
     {
       "aspect_type": "sextile",
       "orb": 1.515303153847185,
       "peak_activations": null,
       "point1": "Venus",
       "point2": "Saturn"
     },
     {
       "aspect_type": "quintile",
       "orb": 0.6309074586280303,
       "peak_activations": null,
       "point1": "Venus",
       "point2": "Neptune"
     },
     {
       "aspect_type": "trine",
       "orb": 6.504330372099844,
       "peak_activations": null,
       "point1": "Venus",
       "point2": "Pluto"
     },
     {
       "aspect_type": "opposition",
       "orb": -1.980076295749683,
       "peak_activations": null,
       "point1": "Mars",
       "point2": "Jupiter"
     },
     {
       "aspect_type": "conjunction",
       "orb": 0.8983625475664212,
       "peak_activations": null,
       "point1": "Mars",
       "point2": "Neptune"
     },
     {
       "aspect_type": "square",
       "orb": -2.114056636541193,
       "peak_activations": null,
       "point1": "Mars",
       "point2": "Mean_Lilith"
     },
     {
       "aspect_type": "quintile",
       "orb": 0.2462811731842578,
       "peak_activations": null,
       "point1": "Mars",
       "point2": "Mean_South_Node"
     },
     {
       "aspect_type": "opposition",
       "orb": -2.878438843316104,
       "peak_activations": null,
       "point1": "Jupiter",
       "point2": "Neptune"
     },
     {
       "aspect_type": "square",
       "orb": 0.13398034079149568,
       "peak_activations": null,
       "point1": "Jupiter",
       "point2": "Mean_Lilith"
     },
     {
       "aspect_type": "trine",
       "orb": -5.23045945568569,
       "peak_activations": null,
       "point1": "Saturn",
       "point2": "Uranus"
     },
     {
       "aspect_type": "opposition",
       "orb": -8.019633525947,
       "peak_activations": null,
       "point1": "Saturn",
       "point2": "Pluto"
     },
     {
       "aspect_type": "quintile",
       "orb": 1.2500929816326902,
       "peak_activations": null,
       "point1": "Uranus",
       "point2": "Pluto"
     },
     {
       "aspect_type": "square",
       "orb": -2.521313788911584,
       "peak_activations": null,
       "point1": "Uranus",
       "point2": "Mean_Node"
     },
     {
       "aspect_type": "square",
       "orb": 2.5213137889115558,
       "peak_activations": null,
       "point1": "Uranus",
       "point2": "Mean_South_Node"
     },
     {
       "aspect_type": "square",
       "orb": -3.012419184107614,
       "peak_activations": null,
       "point1": "Neptune",
       "point2": "Mean_Lilith"
     },
     {
       "aspect_type": "quintile",
       "orb": 1.144643720750679,
       "peak_activations": null,
       "point1": "Neptune",
       "point2": "Mean_South_Node"
     },
     {
       "aspect_type": "trine",
       "orb": -7.774077650636116,
       "peak_activations": null,
       "point1": "Chiron",
       "point2": "Mean_Lilith"
     }
   ],
   "fixed_stars": null,
   "house_cusps": [
     {
       "absolute_longitude": 2.52,
       "degree": 2.52,
       "house": 1,
       "retrograde": null,
       "sign": "Ari"
     },
     {
       "absolute_longitude": 52.14,
       "degree": 22.14,
       "house": 2,
       "retrograde": null,
       "sign": "Tau"
     },
     {
       "absolute_longitude": 74.35,
       "degree": 14.35,
       "house": 3,
       "retrograde": null,
       "sign": "Gem"
     },
     {
       "absolute_longitude": 90.81,
       "degree": 0.81,
       "house": 4,
       "retrograde": null,
       "sign": "Can"
     },
     {
       "absolute_longitude": 107.43,
       "degree": 17.43,
       "house": 5,
       "retrograde": null,
       "sign": "Can"
     },
     {
       "absolute_longitude": 130.37,
       "degree": 10.37,
       "house": 6,
       "retrograde": null,
       "sign": "Leo"
     },
     {
       "absolute_longitude": 182.52,
       "degree": 2.52,
       "house": 7,
       "retrograde": null,
       "sign": "Lib"
     },
     {
       "absolute_longitude": 232.14,
       "degree": 22.14,
       "house": 8,
       "retrograde": null,
       "sign": "Sco"
     },
     {
       "absolute_longitude": 254.35,
       "degree": 14.35,
       "house": 9,
       "retrograde": null,
       "sign": "Sag"
     },
     {
       "absolute_longitude": 270.81,
       "degree": 0.81,
       "house": 10,
       "retrograde": null,
       "sign": "Cap"
     },
     {
       "absolute_longitude": 287.43,
       "degree": 17.43,
       "house": 11,
       "retrograde": null,
       "sign": "Cap"
     },
     {
       "absolute_longitude": 310.37,
       "degree": 10.37,
       "house": 12,
       "retrograde": null,
       "sign": "Aqu"
     }
   ],
   "planetary_positions": [
     {
       "absolute_longitude": 51.85,
       "degree": 21.85,
       "house": 1,
       "is_retrograde": false,
       "name": "Sun",
       "sign": "Tau",
       "speed": 0.9652
     },
     {
       "absolute_longitude": 187.55,
       "degree": 7.55,
       "house": 7,
       "is_retrograde": false,
       "name": "Moon",
       "sign": "Lib",
       "speed": 14.6976
     },
     {
       "absolute_longitude": 43.03,
       "degree": 13.03,
       "house": 1,
       "is_retrograde": true,
       "name": "Mercury",
       "sign": "Tau",
       "speed": -0.4885
     },
     {
       "absolute_longitude": 25.81,
       "degree": 25.81,
       "house": 1,
       "is_retrograde": false,
       "name": "Venus",
       "sign": "Ari",
       "speed": 1.2121
     },
     {
       "absolute_longitude": 312.29,
       "degree": 12.29,
       "house": 12,
       "is_retrograde": false,
       "name": "Mars",
       "sign": "Aqu",
       "speed": 0.5635
     },
     {
       "absolute_longitude": 130.31,
       "degree": 10.31,
       "house": 5,
       "is_retrograde": false,
       "name": "Jupiter",
       "sign": "Leo",
       "speed": 0.1098
     },
     {
       "absolute_longitude": 87.33,
       "degree": 27.33,
       "house": 3,
       "is_retrograde": false,
       "name": "Saturn",
       "sign": "Gem",
       "speed": 0.1142
     }
   ]
 },
 "subject_data": {
   "ascendant": {
     "abs_pos": 2.521476191723111,
     "element": "Fire",
     "emoji": "♈️",
     "house": "First_House",
     "name": "Ascendant",
     "point_type": "AxialCusps",
     "position": 2.521476191723111,
     "quality": "Cardinal",
     "retrograde": false,
     "sign": "Ari",
     "sign_num": 0
   },
   "axial_cusps_names_list": [
     "Ascendant",
     "Descendant",
     "Medium_Coeli",
     "Imum_Coeli"
   ],
   "chiron": {
     "abs_pos": 287.94537910802796,
     "element": "Earth",
     "emoji": "♑️",
     "house": "Eleventh_House",
     "name": "Chiron",
     "point_type": "Planet",
     "position": 17.945379108027964,
     "quality": "Cardinal",
     "retrograde": true,
     "sign": "Cap",
     "sign_num": 9
   },
   "city": "kolomna",
   "day": 13,
   "descendant": {
     "abs_pos": 182.5214761917231,
     "element": "Air",
     "emoji": "♎️",
     "house": "Seventh_House",
     "name": "Descendant",
     "point_type": "AxialCusps",
     "position": 2.52147619172311,
     "quality": "Cardinal",
     "retrograde": false,
     "sign": "Lib",
     "sign_num": 6
   },
   "eighth_house": {
     "abs_pos": 232.14036168247685,
     "element": "Water",
     "emoji": "♏️",
     "house": null,
     "name": "Eighth_House",
     "point_type": "House",
     "position": 22.14036168247685,
     "quality": "Fixed",
     "retrograde": null,
     "sign": "Sco",
     "sign_num": 7
   },
   "eleventh_house": {
     "abs_pos": 287.42577290668953,
     "element": "Earth",
     "emoji": "♑️",
     "house": null,
     "name": "Eleventh_House",
     "point_type": "House",
     "position": 17.42577290668953,
     "quality": "Cardinal",
     "retrograde": null,
     "sign": "Cap",
     "sign_num": 9
   },
   "fifth_house": {
     "abs_pos": 107.42577290668953,
     "element": "Water",
     "emoji": "♋️",
     "house": null,
     "name": "Fifth_House",
     "point_type": "House",
     "position": 17.42577290668953,
     "quality": "Cardinal",
     "retrograde": null,
     "sign": "Can",
     "sign_num": 3
   },
   "first_house": {
     "abs_pos": 2.521476191723111,
     "element": "Fire",
     "emoji": "♈️",
     "house": null,
     "name": "First_House",
     "point_type": "House",
     "position": 2.521476191723111,
     "quality": "Cardinal",
     "retrograde": null,
     "sign": "Ari",
     "sign_num": 0
   },
   "fourth_house": {
     "abs_pos": 90.8050726022056,
     "element": "Water",
     "emoji": "♋️",
     "house": null,
     "name": "Fourth_House",
     "point_type": "House",
     "position": 0.8050726022055983,
     "quality": "Cardinal",
     "retrograde": null,
     "sign": "Can",
     "sign_num": 3
   },
   "hour": 4,
   "houses_names_list": [
     "First_House",
     "Second_House",
     "Third_House",
     "Fourth_House",
     "Fifth_House",
     "Sixth_House",
     "Seventh_House",
     "Eighth_House",
     "Ninth_House",
     "Tenth_House",
     "Eleventh_House",
     "Twelfth_House"
   ],
   "houses_system_identifier": "P",
   "houses_system_name": "Placidus",
   "imum_coeli": {
     "abs_pos": 90.8050726022056,
     "element": "Water",
     "emoji": "♋️",
     "house": "Fourth_House",
     "name": "Imum_Coeli",
     "point_type": "AxialCusps",
     "position": 0.8050726022055983,
     "quality": "Cardinal",
     "retrograde": false,
     "sign": "Can",
     "sign_num": 3
   },
   "iso_formatted_local_datetime": "2003-05-13T04:07:00+04:00",
   "iso_formatted_utc_datetime": "2003-05-13T00:07:00+00:00",
   "julian_day": 2452772.5048611113,
   "jupiter": {
     "abs_pos": 130.30528179818336,
     "element": "Fire",
     "emoji": "♌️",
     "house": "Fifth_House",
     "name": "Jupiter",
     "point_type": "Planet",
     "position": 10.305281798183358,
     "quality": "Fixed",
     "retrograde": false,
     "sign": "Leo",
     "sign_num": 4
   },
   "lat": 55.07108,
   "lng": 38.78399,
   "local_time": 4.116666666666666,
   "lunar_phase": {
     "degrees_between_s_m": 135.70520160480248,
     "moon_emoji": "🌔",
     "moon_phase": 11,
     "moon_phase_name": "Waxing Gibbous",
     "sun_phase": 10
   },
   "mars": {
     "abs_pos": 312.28535809393304,
     "element": "Air",
     "emoji": "♒️",
     "house": "Twelfth_House",
     "name": "Mars",
     "point_type": "Planet",
     "position": 12.285358093933041,
     "quality": "Fixed",
     "retrograde": false,
     "sign": "Aqu",
     "sign_num": 10
   },
   "mean_lilith": {
     "abs_pos": 40.17130145739186,
     "element": "Earth",
     "emoji": "♉️",
     "house": "First_House",
     "name": "Mean_Lilith",
     "point_type": "Planet",
     "position": 10.171301457391863,
     "quality": "Fixed",
     "retrograde": false,
     "sign": "Tau",
     "sign_num": 1
   },
   "mean_node": {
     "abs_pos": 60.039076920748776,
     "element": "Air",
     "emoji": "♊️",
     "house": "Second_House",
     "name": "Mean_Node",
     "point_type": "Planet",
     "position": 0.039076920748776445,
     "quality": "Mutable",
     "retrograde": true,
     "sign": "Gem",
     "sign_num": 2
   },
   "mean_south_node": {
     "abs_pos": 240.03907692074878,
     "element": "Fire",
     "emoji": "♐️",
     "house": "Eighth_House",
     "name": "Mean_South_Node",
     "point_type": "Planet",
     "position": 0.03907692074878355,
     "quality": "Mutable",
     "retrograde": true,
     "sign": "Sag",
     "sign_num": 8
   },
   "medium_coeli": {
     "abs_pos": 270.8050726022056,
     "element": "Earth",
     "emoji": "♑️",
     "house": "Tenth_House",
     "name": "Medium_Coeli",
     "point_type": "AxialCusps",
     "position": 0.8050726022055983,
     "quality": "Cardinal",
     "retrograde": false,
     "sign": "Cap",
     "sign_num": 9
   },
   "mercury": {
     "abs_pos": 43.02588968354249,
     "element": "Earth",
     "emoji": "♉️",
     "house": "First_House",
     "name": "Mercury",
     "point_type": "Planet",
     "position": 13.025889683542488,
     "quality": "Fixed",
     "retrograde": true,
     "sign": "Tau",
     "sign_num": 1
   },
   "minute": 7,
   "month": 5,
   "moon": {
     "abs_pos": 187.55255812506832,
     "element": "Air",
     "emoji": "♎️",
     "house": "Seventh_House",
     "name": "Moon",
     "point_type": "Planet",
     "position": 7.552558125068316,
     "quality": "Cardinal",
     "retrograde": false,
     "sign": "Lib",
     "sign_num": 6
   },
   "name": "Matvey",
   "nation": "RU",
   "neptune": {
     "abs_pos": 313.18372064149946,
     "element": "Air",
     "emoji": "♒️",
     "house": "Twelfth_House",
     "name": "Neptune",
     "point_type": "Planet",
     "position": 13.183720641499463,
     "quality": "Fixed",
     "retrograde": false,
     "sign": "Aqu",
     "sign_num": 10
   },
   "ninth_house": {
     "abs_pos": 254.3490380121087,
     "element": "Fire",
     "emoji": "♐️",
     "house": null,
     "name": "Ninth_House",
     "point_type": "House",
     "position": 14.349038012108707,
     "quality": "Mutable",
     "retrograde": null,
     "sign": "Sag",
     "sign_num": 8
   },
   "perspective_type": "Apparent Geocentric",
   "planets_names_list": [
     "Sun",
     "Moon",
     "Mercury",
     "Venus",
     "Mars",
     "Jupiter",
     "Saturn",
     "Uranus",
     "Neptune",
     "Pluto",
     "Mean_Node",
     "True_Node",
     "Mean_South_Node",
     "True_South_Node",
     "Chiron",
     "Mean_Lilith"
   ],
   "pluto": {
     "abs_pos": 259.31029772802765,
     "element": "Fire",
     "emoji": "♐️",
     "house": "Ninth_House",
     "name": "Pluto",
     "point_type": "Planet",
     "position": 19.31029772802765,
     "quality": "Mutable",
     "retrograde": true,
     "sign": "Sag",
     "sign_num": 8
   },
   "saturn": {
     "abs_pos": 87.32993125397465,
     "element": "Air",
     "emoji": "♊️",
     "house": "Third_House",
     "name": "Saturn",
     "point_type": "Planet",
     "position": 27.32993125397465,
     "quality": "Mutable",
     "retrograde": false,
     "sign": "Gem",
     "sign_num": 2
   },
   "second_house": {
     "abs_pos": 52.14036168247686,
     "element": "Earth",
     "emoji": "♉️",
     "house": null,
     "name": "Second_House",
     "point_type": "House",
     "position": 22.140361682476858,
     "quality": "Fixed",
     "retrograde": null,
     "sign": "Tau",
     "sign_num": 1
   },
   "seventh_house": {
     "abs_pos": 182.5214761917231,
     "element": "Air",
     "emoji": "♎️",
     "house": null,
     "name": "Seventh_House",
     "point_type": "House",
     "position": 2.52147619172311,
     "quality": "Cardinal",
     "retrograde": null,
     "sign": "Lib",
     "sign_num": 6
   },
   "sidereal_mode": null,
   "sixth_house": {
     "abs_pos": 130.3675893110522,
     "element": "Fire",
     "emoji": "♌️",
     "house": null,
     "name": "Sixth_House",
     "point_type": "House",
     "position": 10.3675893110522,
     "quality": "Fixed",
     "retrograde": null,
     "sign": "Leo",
     "sign_num": 4
   },
   "sun": {
     "abs_pos": 51.84735652026585,
     "element": "Earth",
     "emoji": "♉️",
     "house": "First_House",
     "name": "Sun",
     "point_type": "Planet",
     "position": 21.847356520265848,
     "quality": "Fixed",
     "retrograde": false,
     "sign": "Tau",
     "sign_num": 1
   },
   "tenth_house": {
     "abs_pos": 270.8050726022056,
     "element": "Earth",
     "emoji": "♑️",
     "house": null,
     "name": "Tenth_House",
     "point_type": "House",
     "position": 0.8050726022055983,
     "quality": "Cardinal",
     "retrograde": null,
     "sign": "Cap",
     "sign_num": 9
   },
   "third_house": {
     "abs_pos": 74.34903801210871,
     "element": "Air",
     "emoji": "♊️",
     "house": null,
     "name": "Third_House",
     "point_type": "House",
     "position": 14.349038012108707,
     "quality": "Mutable",
     "retrograde": null,
     "sign": "Gem",
     "sign_num": 2
   },
   "true_node": {
     "abs_pos": 59.48064215061702,
     "element": "Earth",
     "emoji": "♉️",
     "house": "Second_House",
     "name": "True_Node",
     "point_type": "Planet",
     "position": 29.480642150617022,
     "quality": "Fixed",
     "retrograde": true,
     "sign": "Tau",
     "sign_num": 1
   },
   "true_south_node": {
     "abs_pos": 239.48064215061703,
     "element": "Water",
     "emoji": "♏️",
     "house": "Eighth_House",
     "name": "True_South_Node",
     "point_type": "Planet",
     "position": 29.48064215061703,
     "quality": "Fixed",
     "retrograde": true,
     "sign": "Sco",
     "sign_num": 7
   },
   "twelfth_house": {
     "abs_pos": 310.3675893110522,
     "element": "Air",
     "emoji": "♒️",
     "house": null,
     "name": "Twelfth_House",
     "point_type": "House",
     "position": 10.3675893110522,
     "quality": "Fixed",
     "retrograde": null,
     "sign": "Aqu",
     "sign_num": 10
   },
   "tz_str": "Europe/Moscow",
   "uranus": {
     "abs_pos": 332.56039070966034,
     "element": "Water",
     "emoji": "♓️",
     "house": "Twelfth_House",
     "name": "Uranus",
     "point_type": "Planet",
     "position": 2.5603907096603393,
     "quality": "Mutable",
     "retrograde": false,
     "sign": "Pis",
     "sign_num": 11
   },
   "utc_time": 0.11666666666666667,
   "venus": {
     "abs_pos": 25.814628100127493,
     "element": "Fire",
     "emoji": "♈️",
     "house": "First_House",
     "name": "Venus",
     "point_type": "Planet",
     "position": 25.814628100127493,
     "quality": "Cardinal",
     "retrograde": false,
     "sign": "Ari",
     "sign_num": 0
   },
   "year": 2003,
   "zodiac_type": "Tropic"
 }
}

'''