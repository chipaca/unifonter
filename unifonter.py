#!/usr/bin/python3 -SIB
# Copyright 2021 John Lenton
# Licensed under GPLv3, see LICENSE file for details.

import argparse
import itertools
import sys
import unicodedata

__all__ = ("unifonter",)
__version__ = "0.5.0"

KINDS = {
    "b": "Bold",
    "i": "Italic",
    "bi": "Bold Italic",
    "s": "Sans-Serif",
    "bs": "Sans-Serif Bold",
    "is": "Sans-Serif Italic",
    "bis": "Sans-Serif Bold Italic",
    "c": "Script",
    "bc": "Bold Script",
    "d": "Double-Struck",
    "f": "Fraktur",
    "bf": "Bold Fraktur",
    "k": "Small-Caps",
    "m": "Monospace",
    "w": "Fullwidth",
}


def _gen_k_help(dump=True):
    styles = []
    for (k, v) in sorted(KINDS.items()):
        if len(k) == 1:
            styles.append("%s (%s)" % (k, unifonter(v, k)))
    out = ", ".join(styles)
    if dump:
        print(repr(out))
    return out


_k = {
    "b": (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        "ƔƖƱɑɣɩɸʊΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωϝ",
        "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"
        "𝚪𝚰𝚼𝛂𝛄𝛊𝛗𝛖𝚨𝚩𝚪𝚫𝚬𝚭𝚮𝚯𝚰𝚱𝚲𝚳𝚴𝚵𝚶𝚷𝚸𝚺𝚻𝚼𝚽𝚾𝚿𝛀𝛂𝛃𝛄𝛅𝛆𝛇𝛈𝛉𝛊𝛋𝛌𝛍𝛎𝛏𝛐𝛑𝛒𝛔𝛕𝛖𝛗𝛘𝛙𝛚𝟋",
    ),
    "i": (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        "ƔƖƱɑɣɩɸʊΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω",
        "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧"
        "𝛤𝛪𝛶𝛼𝛾𝜄𝜑𝜐𝛢𝛣𝛤𝛥𝛦𝛧𝛨𝛩𝛪𝛫𝛬𝛭𝛮𝛯𝛰𝛱𝛲𝛴𝛵𝛶𝛷𝛸𝛹𝛺𝛼𝛽𝛾𝛿𝜀𝜁𝜂𝜃𝜄𝜅𝜆𝜇𝜈𝜉𝜊𝜋𝜌𝜎𝜏𝜐𝜑𝜒𝜓𝜔",
    ),
    "bi": (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        "ƔƖƱɑɣɩɸʊΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω",
        "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛"
        "𝜞𝜤𝜰𝜶𝜸𝜾𝝋𝝊𝜜𝜝𝜞𝜟𝜠𝜡𝜢𝜣𝜤𝜥𝜦𝜧𝜨𝜩𝜪𝜫𝜬𝜮𝜯𝜰𝜱𝜲𝜳𝜴𝜶𝜷𝜸𝜹𝜺𝜻𝜼𝜽𝜾𝜿𝝀𝝁𝝂𝝃𝝄𝝅𝝆𝝈𝝉𝝊𝝋𝝌𝝍𝝎",
    ),
    "s": (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓",
    ),
    "bs": (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        "ƔƖƱɑɣɩɸʊΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω",
        "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
        "𝝘𝝞𝝪𝝰𝝲𝝸𝞅𝞄𝝖𝝗𝝘𝝙𝝚𝝛𝝜𝝝𝝞𝝟𝝠𝝡𝝢𝝣𝝤𝝥𝝦𝝨𝝩𝝪𝝫𝝬𝝭𝝮𝝰𝝱𝝲𝝳𝝴𝝵𝝶𝝷𝝸𝝹𝝺𝝻𝝼𝝽𝝾𝝿𝞀𝞂𝞃𝞄𝞅𝞆𝞇𝞈",
    ),
    "is": (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
    ),
    "bis": (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        "ƔƖƱɑɣɩɸʊΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω",
        "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯"
        "𝞒𝞘𝞤𝞪𝞬𝞲𝞿𝞾𝞐𝞑𝞒𝞓𝞔𝞕𝞖𝞗𝞘𝞙𝞚𝞛𝞜𝞝𝞞𝞟𝞠𝞢𝞣𝞤𝞥𝞦𝞧𝞨𝞪𝞫𝞬𝞭𝞮𝞯𝞰𝞱𝞲𝞳𝞴𝞵𝞶𝞷𝞸𝞹𝞺𝞼𝞽𝞾𝞿𝟀𝟁𝟂",
    ),
    "c": (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏",
    ),
    "bc": (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃",
    ),
    "d": (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzƔɣΓΠΣγπ",
        "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫ℾℽℾℿ⅀ℽℼ",
    ),
    "f": (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
    ),
    "bf": (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟",
    ),
    "m": (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣",
    ),
    "w": (
        " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¢£¥¦¬₩⦅⦆",
        "\u3000！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～￠￡￥￤￢￦｟｠",
    ),
}

_unidata_version = int(unicodedata.unidata_version[: unicodedata.unidata_version.index(".")])
if _unidata_version >= 11:
    # small-caps q is only there since unicode 11 🤷
    _k["k"] = (
        "abcdefghijklmnopqrstuvwyzæðȣʒγλπρψω",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘꞯʀꜱᴛᴜᴠᴡʏᴢᴁᴆᴕᴣᴦᴧᴨᴩᴪꭥ",
    )
else:
    # … so use LATIN SMALL LETTER O WITH OGONEK instead
    _k["k"] = (
        "abcdefghijklmnopqrstuvwyzæðȣʒγλπρψω",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡʏᴢᴁᴆᴕᴣᴦᴧᴨᴩᴪꭥ",
    )


def unifonter(arg, kind):
    if len(_k[kind]) == 2:
        _k[kind] = str.maketrans(*_k[kind])

    arg = unicodedata.normalize("NFKD", arg)
    return arg.translate(_k[kind])


def demo(text, output):
    print(" USE  TO GET", file=output)
    if len(text) == 0:
        for k in KINDS:
            print(" %3s  %s" % (k, unifonter(KINDS[k], k)), file=output)
    else:
        for k in KINDS:
            print(" %3s  %s" % (k, unifonter(" ".join(text), k)), file=output)


_k_help = (
    "b (𝐁𝐨𝐥𝐝), "
    "c (𝒮𝒸𝓇𝒾𝓅𝓉), "
    "d (𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜), "
    "f (𝔉𝔯𝔞𝔨𝔱𝔲𝔯), "
    "i (𝐼𝑡𝑎𝑙𝑖𝑐), "
    "k (Sᴍᴀʟʟ-Cᴀᴘꜱ), "
    "m (𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎), "
    "s (𝖲𝖺𝗇𝗌-𝖲𝖾𝗋𝗂𝖿), "
    "w (Ｆｕｌｌｗｉｄｔｈ)"
)


def main():
    parser = argparse.ArgumentParser(
        description="%(prog)s is a filter that tries to make ASCII fancy with the help of Unicode.",
        epilog="""For starters just run
   %(prog)s -d
and then perhaps
   %(prog)s -d hello world
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i",
        type=argparse.FileType("r"),
        help="read from this file after the positional arguments",
        dest="input",
    )
    parser.add_argument(
        "-o",
        type=argparse.FileType("w"),
        help="write the fancy text to this file (default: stdout)",
        default=sys.stdout,
        dest="output",
    )
    parser.add_argument(
        "-d",
        help="'demo' mode; show your text in all styles, or list all working style combinations if no text given",
        dest="demo",
        action="store_true",
    )
    parser.add_argument(
        "-k",
        help="font style to use; one or more of of "
        + _k_help
        + " (default: random; not all combinations will work; see -d)",
        dest="kind",
    )
    parser.add_argument(
        "-v",
        help="print version and exit.",
        dest="version",
        action="store_true",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="the text to transform. If not given, default -i to stdin",
    )
    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)
    if args.demo:
        if args.input is not None:
            parser.error("currently demo mode only supports arguments, not -i")
        demo(args.text, args.output)
        sys.exit(0)

    if args.kind is None:
        import random

        random.seed()
        kind = random.choice(list(KINDS))
    else:
        kind = args.kind
        if len(kind) > 1:
            kind = "".join(sorted(kind))
        if kind not in KINDS:
            parser.error("unknown kind {!r}".format(args.kind))

    if len(args.text) == 0:
        if args.input is not None:
            it = args.input
        else:
            if sys.stdin.isatty():
                print("reading from stdin", file=sys.stderr)
            it = sys.stdin
    else:
        it = " ".join(args.text) + "\n"
        if args.input is not None:
            it = itertools.chain(it, args.input)

    try:
        for arg in it:
            print(unifonter(arg, kind), file=args.output, end="")
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    main()
