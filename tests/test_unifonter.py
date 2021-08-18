import io
from itertools import chain
from random import shuffle
import unittest

from unifonter import (
    ALIASES,
    KINDS,
    LONG_KINDS,
    _extra_kind_help,
    _k_help,
    _unidata_version,
    demo,
    parse_kind,
    unifonter,
)

from_ascii = "0123456789 abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"

to_ascii = {
    "b": "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗 𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳 𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",
    "i": "0123456789 𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧 𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍",
    "bi": "0123456789 𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛 𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁",
    "s": "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫 𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓 𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹",
    "bs": "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵 𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇 𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭",
    "is": "0123456789 𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻 𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡",
    "bis": "0123456789 𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯 𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕",
    "c": "0123456789 𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏 𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",
    "bc": "0123456789 𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃 𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
    "d": "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡 𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫 𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",
    "f": "0123456789 𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷 𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",
    "bf": "0123456789 𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟 𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",
    "k": "0123456789 ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘꞯʀꜱᴛᴜᴠᴡxʏᴢ ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "m": "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿 𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣 𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
    # NOTE the fullwidth spaces here:
    "w": "０１２３４５６７８９\u3000ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ\u3000ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
}

if _unidata_version < 11:
    to_ascii["k"] = to_ascii["k"].replace("ꞯ", "ǫ")

from_greek = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρςστυφχψω"
to_greek = {
    "b": "𝚨𝚩𝚪𝚫𝚬𝚭𝚮𝚯𝚰𝚱𝚲𝚳𝚴𝚵𝚶𝚷𝚸𝚺𝚻𝚼𝚽𝚾𝚿𝛀𝛂𝛃𝛄𝛅𝛆𝛇𝛈𝛉𝛊𝛋𝛌𝛍𝛎𝛏𝛐𝛑𝛒ς𝛔𝛕𝛖𝛗𝛘𝛙𝛚",
    "i": "𝛢𝛣𝛤𝛥𝛦𝛧𝛨𝛩𝛪𝛫𝛬𝛭𝛮𝛯𝛰𝛱𝛲𝛴𝛵𝛶𝛷𝛸𝛹𝛺𝛼𝛽𝛾𝛿𝜀𝜁𝜂𝜃𝜄𝜅𝜆𝜇𝜈𝜉𝜊𝜋𝜌ς𝜎𝜏𝜐𝜑𝜒𝜓𝜔",
    "bi": "𝜜𝜝𝜞𝜟𝜠𝜡𝜢𝜣𝜤𝜥𝜦𝜧𝜨𝜩𝜪𝜫𝜬𝜮𝜯𝜰𝜱𝜲𝜳𝜴𝜶𝜷𝜸𝜹𝜺𝜻𝜼𝜽𝜾𝜿𝝀𝝁𝝂𝝃𝝄𝝅𝝆ς𝝈𝝉𝝊𝝋𝝌𝝍𝝎",
    "bs": "𝝖𝝗𝝘𝝙𝝚𝝛𝝜𝝝𝝞𝝟𝝠𝝡𝝢𝝣𝝤𝝥𝝦𝝨𝝩𝝪𝝫𝝬𝝭𝝮𝝰𝝱𝝲𝝳𝝴𝝵𝝶𝝷𝝸𝝹𝝺𝝻𝝼𝝽𝝾𝝿𝞀ς𝞂𝞃𝞄𝞅𝞆𝞇𝞈",
    "bis": "𝞐𝞑𝞒𝞓𝞔𝞕𝞖𝞗𝞘𝞙𝞚𝞛𝞜𝞝𝞞𝞟𝞠𝞢𝞣𝞤𝞥𝞦𝞧𝞨𝞪𝞫𝞬𝞭𝞮𝞯𝞰𝞱𝞲𝞳𝞴𝞵𝞶𝞷𝞸𝞹𝞺ς𝞼𝞽𝞾𝞿𝟀𝟁𝟂",
    "d": "ΑΒℾΔΕΖΗΘΙΚΛΜΝΞΟℿΡ⅀ΤΥΦΧΨΩαβℽδεζηθικλμνξοℼρςστυφχψω",  # very low coverage :-(
    "k": "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβᴦδεζηθικᴧμνξοᴨᴩςστυφχᴪꭥ",  # ditto :'(
}


class TestUnifonter(unittest.TestCase):
    def test_ascii(self):
        for kind, expected in to_ascii.items():
            with self.subTest(kind=kind):
                self.assertEqual(unifonter(from_ascii, kind), expected)

    def test_greek(self):
        for kind, expected in to_greek.items():
            with self.subTest(kind=kind):
                self.assertEqual(unifonter(from_greek, kind), expected)

    def test_decomposition(self):
        self.assertEqual(unifonter("árbol", "d"), "𝕒́𝕣𝕓𝕠𝕝")

    def test_demo_no_arg(self):
        f = io.StringIO()
        demo("", f)
        self.assertEqual(
            f.getvalue(),
            """\
  USE               OR   TO GET
  bold              b    𝐁𝐨𝐥𝐝
  italic            i    𝐼𝑡𝑎𝑙𝑖𝑐
  bold italic       bi   𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄
  sans              s    𝖲𝖺𝗇𝗌-𝖲𝖾𝗋𝗂𝖿
  bold sans         bs   𝗦𝗮𝗻𝘀-𝗦𝗲𝗿𝗶𝗳 𝗕𝗼𝗹𝗱
  italic sans       is   𝘚𝘢𝘯𝘴-𝘚𝘦𝘳𝘪𝘧 𝘐𝘵𝘢𝘭𝘪𝘤
  bold italic sans  bis  𝙎𝙖𝙣𝙨-𝙎𝙚𝙧𝙞𝙛 𝘽𝙤𝙡𝙙 𝙄𝙩𝙖𝙡𝙞𝙘
  script            c    𝒮𝒸𝓇𝒾𝓅𝓉
  bold script       bc   𝓑𝓸𝓵𝓭 𝓢𝓬𝓻𝓲𝓹𝓽
  double-struck     d    𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜
  fraktur           f    𝔉𝔯𝔞𝔨𝔱𝔲𝔯
  bold fraktur      bf   𝕭𝖔𝖑𝖉 𝕱𝖗𝖆𝖐𝖙𝖚𝖗
  small-caps        k    Sᴍᴀʟʟ-Cᴀᴘꜱ
  mono              m    𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎
  wide              w    Ｆｕｌｌｗｉｄｔｈ
"""
            + _extra_kind_help,
        )

    def test_demo_w_arg(self):
        f = io.StringIO()
        demo("Hello", f)
        self.assertEqual(
            f.getvalue(),
            """\
  USE               OR   TO GET
  bold              b    𝐇𝐞𝐥𝐥𝐨
  italic            i    𝐻𝑒𝑙𝑙𝑜
  bold italic       bi   𝑯𝒆𝒍𝒍𝒐
  sans              s    𝖧𝖾𝗅𝗅𝗈
  bold sans         bs   𝗛𝗲𝗹𝗹𝗼
  italic sans       is   𝘏𝘦𝘭𝘭𝘰
  bold italic sans  bis  𝙃𝙚𝙡𝙡𝙤
  script            c    ℋℯ𝓁𝓁ℴ
  bold script       bc   𝓗𝓮𝓵𝓵𝓸
  double-struck     d    ℍ𝕖𝕝𝕝𝕠
  fraktur           f    ℌ𝔢𝔩𝔩𝔬
  bold fraktur      bf   𝕳𝖊𝖑𝖑𝖔
  small-caps        k    Hᴇʟʟᴏ
  mono              m    𝙷𝚎𝚕𝚕𝚘
  wide              w    Ｈｅｌｌｏ
"""
            + _extra_kind_help,
        )

    def test_kinds(self):
        # test that the kinds are stored sorted
        for k in KINDS:
            with self.subTest(kind=k):
                self.assertTrue(k == "".join(sorted(k)))

    def test_long_kinds(self):
        self.assertEqual(len(KINDS), len(LONG_KINDS))
        # test that the long kinds are stored sorted
        for k in LONG_KINDS:
            if k == "small-caps":
                continue
            with self.subTest(kind=k):
                self.assertTrue(k == "+".join(sorted(k.split("+"))))

    def test_aliases(self):
        # test that the aliases are stored sorted
        for k in ALIASES:
            with self.subTest(kind=k):
                self.assertTrue(k == "+".join(sorted(k.split("+"))))

    def test_parse_kind(self):
        for k in KINDS:
            with self.subTest(kind=k):
                self.assertEqual(parse_kind(k), k)
        for k, v in chain(LONG_KINDS.items(), ALIASES.items()):
            with self.subTest(kind=k):
                self.assertEqual(parse_kind(k), v)
            k = k.replace(" ", "-")
            for c in " _-+":
                k2 = k.replace("-", c)
                with self.subTest(kind=k2):
                    self.assertEqual(parse_kind(k2), v)

        # single-letter, shuffled:
        for k in KINDS:
            ok = k
            k = list(k)
            shuffle(k)
            for c in " _-+":
                k2 = c.join(k)
                with self.subTest(kind=k2):
                    self.assertEqual(parse_kind(k2), ok)
            k = "".join(k)
            with self.subTest(kind=k):
                self.assertEqual(parse_kind(k), ok)

        # long, mixed, shuffled:
        for k, v in LONG_KINDS.items():
            if " " not in k:
                continue
            k = k.split()
            shuffle(k)
            for c in " _-+":
                k2 = c.join(k)
                with self.subTest(kind=k2):
                    self.assertEqual(parse_kind(k2), v)

        # a few more, not all valid
        self.assertEqual(parse_kind("i bold"), "bi")
        self.assertEqual(parse_kind("bold i"), "bi")
        self.assertEqual(parse_kind("italic b"), "bi")
        self.assertEqual(parse_kind("b italic"), "bi")
        self.assertEqual(parse_kind("script+fraktur"), "cf")
        self.assertEqual(parse_kind("bi+sans"), "bis")
        self.assertEqual(parse_kind("bold-i-double-struck"), "bdi")

        # some bad ones but ignored
        self.assertEqual(parse_kind("caps serif"), "k")
        self.assertEqual(parse_kind("double small struck serif"), "d")

    maxDiff = None
