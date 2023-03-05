import math

HEAVENLYS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLYS = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ANIMALS = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
PALACES = [
    "命宮", "父母", "福德", "田宅", "官祿", "交友",
    "遷移", "疾厄", "財帛", "子女", "夫妻", "兄弟",
]
ROUNDS = ["金四局", "水二局", "火六局", "土五局", "木三局"]


def birth_palace(month: str, hour: str) -> dict:
    """12宮位置
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    input: "卯", "丑"
    output: {'子': '夫妻', '丑': '兄弟', '寅': '命宮',...}

    Args:
        month (str): 出生月 (農曆一月為"寅", 二月為"卯", 以此類推)
        hour (str): 出生時 (前一天23點 ~ 1點為"子", 1點 ~ 3點為"丑", 以此類推)

    Returns:
        dict: 子丑寅卯...對應的12宮
    """
    self_palace = (12 + EARTHLYS.index(month) - EARTHLYS.index(hour)) % 12
    return {
        earthly: PALACES[(12 - self_palace + i) % 12]
        for i, earthly in enumerate(EARTHLYS)
    }


def birth_bodypalace(month: str, hour: str) -> dict:
    """身宮位置
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    input: "卯", "丑"
    output: {"子": False, '丑': False, "寅": False, "卯": False, "辰": True,...}

    Args:
        month (str): 出生月 (農曆一月為"寅", 二月為"卯", 以此類推)
        hour (str): 出生時 (前一天23點 ~ 1點為"子", 1點 ~ 3點為"丑", 以此類推)

    Returns:
        dict: 子丑寅卯...身宮位於該位置 True, 其他為 False
    """
    body_palace = (EARTHLYS.index(month) + EARTHLYS.index(hour)) % 12
    return {
        earthly: bool(earthly == EARTHLYS[body_palace]) for earthly in EARTHLYS
    }


def birth_heavenly(year: str) -> dict:
    """天干位置
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    input: "癸"
    output: {"子": "甲", "丑": "乙", "寅": "甲",...}

    Args:
        year (str): 出生年的天干

    Returns:
        dict: 子丑寅卯...對應的天干
    """
    # 甲己 餘 0 ....  + 2 = 丙(2) => 餘數 + (餘數 + 2) = 0 + 0 + 2 = 2
    # 乙庚 餘 1 ....  + 3 = 戌(4) => 餘數 + (餘數 + 2) = 1 + 1 + 2 = 4
    # 丙辛 餘 2 ....  + 4 = 庚(6) => 餘數 + (餘數 + 2) = 2 + 2 + 2 = 6
    # 丁壬 餘 3 ....  + 5 = 壬(8) => 餘數 + (餘數 + 2) = 3 + 3 + 2 = 8
    # 戊癸 餘 4 ....  + 6 = 甲(0) => 餘數 + (餘數 + 2) = 4 + 4 + 2 = 10
    # => (餘數 * 2 + 2) % 10
    start_index = ((HEAVENLYS.index(year) % 5) * 2 + 2) % 10
    result = {"子": HEAVENLYS[start_index], "丑": HEAVENLYS[start_index + 1]}
    for i in range(10):
        result[EARTHLYS[2 + i]] = HEAVENLYS[(start_index + i) % 10]
    return result


def birth_round(selfpalace_heavenaly: str, selfpalace_earthly: str) -> str:
    """五行局
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    birth_palace("卯", "丑") 得知 "命宮" 位於"寅"
    birth_heavenly("癸") 得知 "甲" 位於"寅"
    input: "甲", "寅"
    output: '水二局'

    Args:
        selfpalace_heavenaly (str): 命宮位置的天干
        selfpalace_earthly (str): 命宮位置的地支

    Returns:
        str: 五行局的字串
    """
    # 子丑 商 0 -> 除以 3 餘 0
    # 寅卯 商 1 -> 除以 3 餘 1
    # 辰巳 商 2 -> 除以 3 餘 2
    # 午未 商 3 -> 除以 3 餘 0
    # 申酉 商 4 -> 除以 3 餘 1
    # 戌亥 商 5 -> 除以 3 餘 2
    # ===========================
    # 甲乙 商 0
    # 丙丁 商 1
    # 戊己 商 2
    # 庚辛 商 3
    # 壬癸 商 4
    # ========================
    # 五行的位置 index 為 0 ~ 4, 所以取餘數
    # (步驟一的餘 + 步驟二的商) % 5
    return ROUNDS[
        (
            (EARTHLYS.index(selfpalace_earthly) // 2 % 3)
            + (HEAVENLYS.index(selfpalace_heavenaly) // 2)
        )
        % 5
    ]


def star_emperor(day: int, round: str) -> str:
    """紫微星位置
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    input: 10, "水二局"
    output: '午'

    Args:
        day (int): 出生日
        round (str): 五行局

    Returns:
        str: 紫微星位置(地支)
    """
    # day 農曆最大30, 遇到水二局, 商為15, index 為 0 ~ 11, 所以取餘數
    # 由寅開始(index = 2)
    cycle = {"金四局": 4, "水二局": 2, "火六局": 6, "土五局": 5, "木三局": 3}[round]
    cell = (2 + math.ceil(day / cycle) - 1) % 12
    lack = cycle - (day % cycle) if day % cycle else 0
    return EARTHLYS[cell + lack * (-1) ** lack]


def stars_main(day: int, round: str) -> dict:
    """十四顆主星
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    input: 10, "水二局"
        star_emperor(10, "水二局") 得知 "紫微" 位於 "午"
    output: {'子': ['貪狼'], '丑': ['天同', '巨門'], '寅': ['武曲', '天相'],...}


    Args:
        day (int): 出生日
        round (str): 五行局

    Returns:
        dict: 子丑寅卯...對應的星曜
    """
    # star_emperor(10, "水二局") 得知 "紫微" 位於 "午"
    # 天府 位於 紫微的對角
    rule_1 = [
        "紫微", None, None, None, "廉貞", None,
        None, "天同", "武曲", "太陽", None, "天機",
    ]
    rule_2 = [
        "天府", "太陰", "貪狼", "巨門", "天相", "天梁",
        "七殺", None, None, None, "破軍", None,
    ]
    rule_1_start = EARTHLYS.index(star_emperor(day, round))
    rule_2_start = ((rule_1_start - 2) * -1 + 12 + 2) % 12
    result = dict()
    for i, earthly in enumerate(EARTHLYS):
        result[earthly] = []
        for rule, start in [(rule_1, rule_1_start), (rule_2, rule_2_start)]:
            if star := rule[(i - start + 12) % 12]:
                result[earthly].append(star)
    return result


def stars_lucky(
        birth_year_heavenaly: str, birth_year_earthly: str,
        birth_month: str, birth_hour: str
    ) -> dict:
    """甲級星的輔星 八吉星
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    input: "癸", "卯", "卯", "丑"
    output: {'子': ['祿存'], '丑': [], '寅': [], '卯': ['天魁'],...}

    Args:
        birth_year_heavenaly (str): 出生年(天干)
        birth_year_earthly (str): 出生年(地支)
        birth_month (str): 出生月(地支)
        birth_hour (str): 出生時(地支)

    Returns:
        dict: 子丑寅卯...對應的星曜
    """
    # 左輔: 以辰起始順時針 (起始值 4 + (寅月(i=2) - 2)) => 2 + 出生月(地支)
    # 右弼: 以戌起始逆時針 (起始值 10 - (寅月(i=2) - 2)) => 12 - 出生月(地支)
    # 文曲: 以辰起始順時針 (起始值 4 + (子時(i=0))) => 4 + 出生時(地支)
    # 文昌: 以戌起始逆時針 (起始值 10 - (子時(i=0))) => 10 - 出生月(地支)
    # 天魁,天鉞: 出生年(天干)
    # 甲(0)戊(4)庚(6) ..... 牛(1),羊(7)
    # 乙(1)己(5)      ..... 鼠(0),猴(8)
    # 丙(2)丁(3)      ..... 豬(11),雞(9)
    # 辛(7)           ..... 馬(6),虎(2)
    # 壬(8)癸(9)      ..... 兔(3),蛇(5)
    # 祿存: 出生年(天干)
    # 甲(0)      ..... 寅(2)
    # 乙(1)      ..... 卯(3)
    # 丙(2)戊(4) ..... 巳(5)
    # 丁(3)已(5) ..... 午(6)
    # 庚(6)      ..... 巳(8)
    # 辛(7)      ..... 午(9)
    # 壬(8)      ..... 亥(11)
    # 癸(9)      ..... 子(0)
    result = {earthly: [] for earthly in EARTHLYS}
    result[EARTHLYS[(2 + EARTHLYS.index(birth_month)) % 12]].append("左輔")
    result[EARTHLYS[(12 - EARTHLYS.index(birth_month)) % 12]].append("右弼")
    result[EARTHLYS[(4 + EARTHLYS.index(birth_hour)) % 12]].append("文曲")
    result[EARTHLYS[(10 - EARTHLYS.index(birth_hour)) % 12]].append("文昌")
    # 天魁, 天鉞, 祿存
    rule = [
        (1, 7, 2), (0, 8, 3), (11, 9, 5), (11, 9, 6), (1, 7, 5),
        (0, 8, 6), (1, 7, 8), (6, 2, 9), (3, 5, 11), (3, 5, 0),
    ]
    star = rule[HEAVENLYS.index(birth_year_heavenaly)]
    result[EARTHLYS[star[0]]].append("天魁")
    result[EARTHLYS[star[1]]].append("天鉞")
    result[EARTHLYS[star[2]]].append("祿存")
    # 天馬
    rule = [2, 11, 8, 5]
    result[EARTHLYS[rule[EARTHLYS.index(birth_year_earthly) % 4]]].append("天馬")
    return result


def stars_unluckly(
        birth_year_heavenaly: str, birth_year_earthly: str, birth_hour: str
    ) -> dict:
    """甲級星的輔星 六煞星
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    input: "癸", "卯", "丑"
    output: {'子': ['地劫'], '丑': ['擎羊'], '寅': [], '卯': [],...}

    Args:
        birth_year_heavenaly (str): 出生年(天干)
        birth_year_earthly (str): 出生年(地支)
        birth_hour (str): 出生時(地支)

    Returns:
        dict: 子丑寅卯...對應的星曜
    """
    result = {earthly: [] for earthly in EARTHLYS}
    birth_year_heavenaly_index = HEAVENLYS.index(birth_year_heavenaly)
    birth_year_earthly_index = EARTHLYS.index(birth_year_earthly)
    birth_hour_index = EARTHLYS.index(birth_hour)
    # 擎羊、陀羅 input: birth_year_heavenaly
    rule = [
        (3, 1), (4, 2), (6, 4), (7, 5), (6, 4),
        (7, 5), (9, 7), (10, 8), (0, 10), (1, 11),
    ]
    result[EARTHLYS[rule[birth_year_heavenaly_index][0]]].append("擎羊")
    result[EARTHLYS[rule[birth_year_heavenaly_index][1]]].append("陀羅")
    # 火星、鈴星 input: birth_year_earthly, birth_hour
    rule = [(2, 10), (3, 10), (1, 3), (9, 10)]
    result[
        EARTHLYS[rule[birth_year_earthly_index % 4][0] + birth_hour_index]
    ].append("火星")
    result[
        EARTHLYS[rule[birth_year_earthly_index % 4][1] + birth_hour_index]
    ].append("鈴星")
    # 地劫、地空 input: birth_hour
    # 地劫: 從 亥宮位開始順時針 11 + (子時=0)
    # 地空: 從 亥宮位開始逆時針 11 - (子時=0)
    result[EARTHLYS[(11 + birth_hour_index) % 12]].append("地劫")
    result[EARTHLYS[(11 - birth_hour_index) % 12]].append("地空")
    return result


def stars_LuQuanKeJi(birth_year_heavenaly: str) -> dict:
    """四化星
    Ex: 出生 2023-03-01 丑時(農曆癸卯年二月初十 丑時)
    input: "癸"
    output: {'祿': '破軍', '權': '巨門', '科': '太陰', '忌': '貪狼'}

    Args:
        birth_year_heavenaly (str): 出生年(天干)

    Returns:
        dict: 四化對應的星曜
    """
    birth_year_heavenaly_index = HEAVENLYS.index(birth_year_heavenaly)
    rule = [
        ("廉貞", "破軍", "武曲", "太陽"), ("天機", "天梁", "紫微", "太陰"),
        ("天同", "天機", "文昌", "廉貞"), ("太陰", "天同", "天機", "巨門"),
        ("貪狼", "太陰", "太陽", "天機"), ("武曲", "貪狼", "天梁", "文曲"),
        ("太陽", "武曲", "天府", "天同"), ("巨門", "太陽", "文曲", "文昌"),
        ("天梁", "紫微", "天府", "武曲"), ("破軍", "巨門", "太陰", "貪狼"),
    ]
    LuQuanKeJi = rule[birth_year_heavenaly_index]
    return dict(zip(("祿", "權", "科", "忌"), LuQuanKeJi))
