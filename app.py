HEAVENLYS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLYS = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ANIMALS = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
PALACES = [
    "命宮", "父母", "福德", "田宅", "官祿", "交友",
    "遷移", "疾厄", "財帛", "子女", "夫妻", "兄弟",
]


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
    result = {"子": HEAVENLYS[start_index], "丑": HEAVENLYS[start_index+1]}
    for i in range(10):
        result[EARTHLYS[2 + i]] = HEAVENLYS[(start_index + i) % 10]
    return result
