import math

HEAVENLYS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLYS = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ANIMALS = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
PALACES = [
    "命宮", "父母", "福德", "田宅", "官祿", "交友",
    "遷移", "疾厄", "財帛", "子女", "夫妻", "兄弟",
]
ROUNDS = ["金四局", "水二局", "火六局", "土五局", "木三局"]


def ROC2HeavenalyEarthly(year: int) -> str:
    """民國換成為天干地支
    ex 2023-03-01 丑時 (民國112年)(農曆癸卯年二月初十 丑時)
    input: 112
    output "癸卯"

    Args:
        year (int): 民國年

    Returns:
        str: 年(天干地支)
    """
    return HEAVENLYS[(7 + year) % 10] + EARTHLYS[(11 + year) % 12]


class BirthChart:
    def __init__(
        self,
        birth_year_heavenaly_earthly: str = "癸卯",
        birth_month: str = "卯",
        birth_day: int = 10,
        birth_hour: str = "丑",
    ):
        self.b_y_he = birth_year_heavenaly_earthly
        self.b_m = birth_month
        self.b_d = birth_day
        self.b_h = birth_hour
        # 出生年
        # 檢查 type, 字串長度, 是否符合規則的字
        if isinstance(self.b_y_he, str | int):
            match self.b_y_he:
                case self.b_y_he if (
                    type(self.b_y_he) == int and self.b_y_he > 0
                ):
                    raise TypeError(
                        f"民國{self.b_y_he}年? "
                        f'您是否想輸入"{ROC2HeavenalyEarthly(self.b_y_he)}"?'
                    )
                case self.b_y_he if type(self.b_y_he) == str:
                    self.b_y_he = self.b_y_he.strip().replace(" ", "")
                    if len(self.b_y_he) == 2:
                        if self.b_y_he[0] not in HEAVENLYS:
                            raise ValueError(
                                f'您輸入的第一個字為"{self.b_y_he[0]}", '
                                "請輸入 甲乙丙丁戊己庚辛壬癸 中的一個字"
                            )
                        if self.b_y_he[1] not in EARTHLYS:
                            raise ValueError(
                                f'您輸入的第二個字為"{self.b_y_he[1]}", '
                                "請輸入 子丑寅卯辰巳午未申酉戌亥 中的一個字"
                            )
                    else:
                        raise ValueError('出生年請輸入兩個字(天干地支) ex "甲子"')
                case _:
                    raise TypeError('出生年請輸入字串(天干地支) ex "甲子"')
        else:
            raise TypeError(f'{type(self.b_y_he)}? 出生年請輸入字串(天干地支) ex "甲子"')
        # 出生月
        # 檢查 type, 字串長度, 是否符合規則的字
        if isinstance(self.b_m, str | int):
            match self.b_m:
                case self.b_m if type(self.b_m) == int and 0 < self.b_m < 13:
                    raise TypeError(
                        f"農曆{self.b_m}月? "
                        f'您是否想輸入"{EARTHLYS[(1 + self.b_m) % 12]}"?'
                    )
                case self.b_m if type(self.b_m) == str:
                    self.b_m = self.b_m.strip().replace(" ", "")
                    if len(self.b_m) == 1:
                        if self.b_m not in EARTHLYS:
                            raise ValueError(
                                f'您輸入的字為"{self.b_m}", '
                                "請輸入 子丑寅卯辰巳午未申酉戌亥 中的一個字"
                            )
                    else:
                        raise ValueError('出生月請輸入一個字(地支) ex "子"')
                case _:
                    raise TypeError('出生月請輸入字串(地支) ex "子"')
        else:
            raise TypeError('出生月請輸入字串(地支) ex "子"')
        # 出生日
        if isinstance(self.b_d, int):
            if self.b_d < 1 or self.b_d > 29:
                raise ValueError("出生日請輸入農曆數字")
        else:
            raise TypeError("出生日請輸入數字 ex 1")
        # 出生時
        # 檢查 type, 字串長度, 是否符合規則的字
        if isinstance(self.b_h, str | int):
            match self.b_h:
                case self.b_h if type(self.b_h) == int and 0 <= self.b_h <= 23:
                    raise TypeError(
                        f"{self.b_h}點? "
                        f'您是否想輸入"{EARTHLYS[((self.b_h + 1) % 24) // 2]}"?'
                    )
                case self.b_h if type(self.b_h) == str:
                    self.b_h = self.b_h.strip().replace(" ", "")
                    if len(self.b_h) == 1:
                        if self.b_h not in EARTHLYS:
                            raise ValueError(
                                f'您輸入的字為"{self.b_h}", '
                                "請輸入 子丑寅卯辰巳午未申酉戌亥 中的一個字"
                            )
                    else:
                        raise ValueError('出生月請輸入一個字(地支) ex "子"')
                case _:
                    raise TypeError('出生時請輸入字串(地支) ex "子"')
        else:
            raise TypeError('出生時請輸入字串(地支) ex "子"')

        self.b_y_h = self.b_y_he[0]
        self.b_y_e = self.b_y_he[1]
        # 天干
        self.b_heavenly = self.birth_heavenly(self.b_y_h)
        # 十二宮
        self.b_palace = self.birth_palace(self.b_m, self.b_h)
        for e, palace in self.b_palace.items():
            if palace == "命宮":
                self.b_selfplace_h = self.b_heavenly[e]
                self.b_selfplace_e = e
                break
        # 五局數
        self.b_round = self.birth_round(self.b_selfplace_h, self.b_selfplace_e)
        # 身宮
        self.b_bodypalace = self.birth_bodypalace(self.b_m, self.b_h)
        # 主星
        self.b_stars_main = self.stars_main(self.b_d, self.b_round)
        # 八吉星
        self.b_stars_lucky = self.stars_lucky(
            self.b_y_h, self.b_y_e, self.b_m, self.b_h
        )
        # 六煞星
        self.b_stars_unlucky = self.stars_unluckly(
            self.b_y_h, self.b_y_e, self.b_h
        )
        # 四化星
        self.b_stars_LuQuanKeJi = self.stars_LuQuanKeJi(self.b_y_h)
        # 排盤
        self.chart = {earthly: {} for earthly in EARTHLYS}
        for earthly in EARTHLYS:
            self.chart[earthly] = {}
            self.chart[earthly]["天干"] = self.b_heavenly[earthly]
            self.chart[earthly]["地支"] = earthly
            self.chart[earthly]["十二宮"] = self.b_palace[earthly]
            self.chart[earthly]["主星"] = self.b_stars_main[earthly]
            self.chart[earthly]["八吉星"] = self.b_stars_lucky[earthly]
            self.chart[earthly]["六煞星"] = self.b_stars_unlucky[earthly]
            for star, LuQuanKeJi in self.b_stars_LuQuanKeJi.items():
                if star in self.chart[earthly]["主星"]:
                    star_index = self.chart[earthly]["主星"].index(star)
                    self.chart[
                        earthly
                    ]["主星"][star_index] = f"{star}[{LuQuanKeJi}]"

    def birth_palace(self, month: str, hour: str) -> dict:
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

    def birth_bodypalace(self, month: str, hour: str) -> dict:
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
            earthly: bool(earthly == EARTHLYS[body_palace])
            for earthly in EARTHLYS
        }

    def birth_heavenly(self, year_heavenaly: str) -> dict:
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
        start_index = (
            (HEAVENLYS.index(year_heavenaly) % 5) * 2 + 2
        ) % 10
        result = {
            "子": HEAVENLYS[start_index],
            "丑": HEAVENLYS[start_index + 1],
        }
        for i in range(10):
            result[EARTHLYS[2 + i]] = HEAVENLYS[(start_index + i) % 10]
        return result

    def birth_round(
        self, selfpalace_heavenaly: str, selfpalace_earthly: str
    ) -> str:
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

    def star_emperor(self, day: int, round: str) -> str:
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

    def stars_main(self, day: int, round: str) -> dict:
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
        rule_1_start = EARTHLYS.index(self.star_emperor(day, round))
        rule_2_start = ((rule_1_start - 2) * -1 + 12 + 2) % 12
        result = dict()
        for i, earthly in enumerate(EARTHLYS):
            result[earthly] = []
            for rule, start in [
                (rule_1, rule_1_start),
                (rule_2, rule_2_start),
            ]:
                if star := rule[(i - start + 12) % 12]:
                    result[earthly].append(star)
        return result

    def stars_lucky(
        self,
        birth_year_heavenaly: str,
        birth_year_earthly: str,
        birth_month: str,
        birth_hour: str,
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
        result[EARTHLYS[rule[EARTHLYS.index(birth_year_earthly) % 4]]].append(
            "天馬"
        )
        return result

    def stars_unluckly(
        self,
        birth_year_heavenaly: str,
        birth_year_earthly: str,
        birth_hour: str,
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
            EARTHLYS[
                (rule[birth_year_earthly_index % 4][0] + birth_hour_index) % 12
            ]
        ].append("火星")
        result[
            EARTHLYS[
                (rule[birth_year_earthly_index % 4][1] + birth_hour_index) % 12
            ]
        ].append("鈴星")
        # 地劫、地空 input: birth_hour
        # 地劫: 從 亥宮位開始順時針 11 + (子時=0)
        # 地空: 從 亥宮位開始逆時針 11 - (子時=0)
        result[EARTHLYS[(11 + birth_hour_index) % 12]].append("地劫")
        result[EARTHLYS[(11 - birth_hour_index) % 12]].append("地空")
        return result

    def stars_LuQuanKeJi(self, birth_year_heavenaly: str) -> dict:
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
            ("廉貞", "破軍", "武曲", "太陽"),
            ("天機", "天梁", "紫微", "太陰"),
            ("天同", "天機", "文昌", "廉貞"),
            ("太陰", "天同", "天機", "巨門"),
            ("貪狼", "太陰", "右弼", "天機"),
            ("武曲", "貪狼", "天梁", "文曲"),
            ("太陽", "武曲", "太陰", "天同"),
            ("巨門", "太陽", "文曲", "文昌"),
            ("天梁", "紫微", "左輔", "武曲"),
            ("破軍", "巨門", "太陰", "貪狼"),
        ]
        LuQuanKeJi = rule[birth_year_heavenaly_index]
        return dict(zip(LuQuanKeJi, ("祿", "權", "科", "忌")))
