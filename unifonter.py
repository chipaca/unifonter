# Copyright 2021 John Lenton
# Licensed under GPLv3, see LICENSE file for details.

import argparse
import itertools
import re
import sys
import unicodedata

__all__ = ("unifonter", "KINDS")
__version__ = "0.0.1"

KINDS = {
    "b": "BOLD",
    "i": "ITALIC",
    "bi": "BOLD ITALIC",
    "s": "SANS-SERIF",
    "bs": "SANS-SERIF BOLD",
    "is": "SANS-SERIF ITALIC",
    "bis": "SANS-SERIF BOLD ITALIC",
    "c": "SCRIPT",
    "bc": "BOLD SCRIPT",
    "d": "DOUBLE-STRUCK",
    "f": "FRAKTUR",
    "bf": "BOLD FRAKTUR",
    "k": "SMALL-CAPS",
    "m": "MONOSPACE",
    "w": "FULLWIDTH",
}

_EXCEPTIONS = {
    "FULLWIDTH SPACE": "\u3000",  # IDEOGRAPHIC SPACE
    "MATHEMATICAL SCRIPT SMALL E": "ℯ",  # SCRIPT SMALL E
    "MATHEMATICAL SCRIPT SMALL O": "ℴ",  # SCRIPT SMALL O
    "MATHEMATICAL SCRIPT SMALL G": "ℊ",  # SCRIPT SMALL G
    "MATHEMATICAL SCRIPT CAPITAL B": "ℬ",  # SCRIPT CAPITAL B
    "MATHEMATICAL SCRIPT CAPITAL E": "ℰ",  # SCRIPT CAPITAL E
    "MATHEMATICAL SCRIPT CAPITAL F": "ℱ",  # SCRIPT CAPITAL F
    "MATHEMATICAL SCRIPT CAPITAL H": "ℋ",  # SCRIPT CAPITAL H
    "MATHEMATICAL SCRIPT CAPITAL I": "ℐ",  # SCRIPT CAPITAL I
    "MATHEMATICAL SCRIPT CAPITAL L": "ℒ",  # SCRIPT CAPITAL L
    "MATHEMATICAL SCRIPT CAPITAL M": "ℳ",  # SCRIPT CAPITAL M
    "MATHEMATICAL SCRIPT CAPITAL R": "ℛ",  # SCRIPT CAPITAL R
    "MATHEMATICAL FRAKTUR CAPITAL C": "ℭ",  # BLACK-LETTER CAPITAL C
    "MATHEMATICAL FRAKTUR CAPITAL H": "ℌ",  # BLACK-LETTER CAPITAL H
    "MATHEMATICAL FRAKTUR CAPITAL I": "ℑ",  # BLACK-LETTER CAPITAL I
    "MATHEMATICAL FRAKTUR CAPITAL R": "ℜ",  # BLACK-LETTER CAPITAL R
    "MATHEMATICAL FRAKTUR CAPITAL Z": "ℨ",  # BLACK-LETTER CAPITAL Z
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL C": "ℂ",  # DOUBLE-STRUCK CAPITAL C
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL H": "ℍ",  # DOUBLE-STRUCK CAPITAL H
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL N": "ℕ",  # DOUBLE-STRUCK CAPITAL N
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL P": "ℙ",  # DOUBLE-STRUCK CAPITAL P
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL Q": "ℚ",  # DOUBLE-STRUCK CAPITAL Q
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL R": "ℝ",  # DOUBLE-STRUCK CAPITAL R
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL Z": "ℤ",  # DOUBLE-STRUCK CAPITAL Z
    "MATHEMATICAL ITALIC SMALL H": "ℎ",  # PLANCK CONSTANT
}

if int(unicodedata.unidata_version[: unicodedata.unidata_version.index(".")]) < 11:
    # this one's only there since unicode 11 🤷
    _EXCEPTIONS[
        "LATIN LETTER SMALL CAPITAL Q"
    ] = "ǫ"  # LATIN SMALL LETTER O WITH OGONEK


def _gen_k_help(dump=True):
    styles = []
    for (k, v) in sorted(KINDS.items()):
        if len(k) == 1:
            styles.append("%s (%s)" % (k, unifonter(v.title(), KINDS[k])))
    out = ", ".join(styles)
    if dump:
        print(repr(out))
    return out


_rx = re.compile(r"^LATIN (\S+) LETTER (\S+)$")


def unifonter(arg, kind):
    s = []
    nrepl = "MATHEMATICAL %s " % (kind,)
    if kind == "SMALL-CAPS":
        lrepl = r"LATIN LETTER \1 CAPITAL \2"
    else:
        lrepl = r"MATHEMATICAL %s \1 \2" % (kind,)

    for lraw in arg:
        for l in unicodedata.normalize("NFKD", lraw):
            try:
                name = unicodedata.name(l)
                if kind == "FULLWIDTH":
                    name = "FULLWIDTH " + name
                else:
                    if name.startswith("DIGIT "):
                        name = nrepl + name
                    else:
                        name = _rx.sub(lrepl, name)
                if name in _EXCEPTIONS:
                    s.append(_EXCEPTIONS[name])
                else:
                    s.append(unicodedata.lookup(name))
            except (ValueError, KeyError):
                s.append(l)
    return "".join(s)


def demo(text):
    print(" USE  TO GET")
    if len(text) == 0:
        for k in KINDS:
            print(" %3s  %s" % (k, unifonter(KINDS[k].title(), KINDS[k])))
    else:
        for k in KINDS:
            print(" %3s  %s" % (k, unifonter(" ".join(text), KINDS[k])))


_k_help = "b (𝐁𝐨𝐥𝐝), c (𝒮𝒸𝓇𝒾𝓅𝓉), d (𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜), f (𝔉𝔯𝔞𝔨𝔱𝔲𝔯), i (𝐼𝑡𝑎𝑙𝑖𝑐), k (Sᴍᴀʟʟ-Cᴀᴘꜱ), m (𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎), s (𝖲𝖺𝗇𝗌-𝖲𝖾𝗋𝗂𝖿), w (Ｆｕｌｌｗｉｄｔｈ)"


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
        "text",
        nargs="*",
        help="the text to transform. If not given, default -i to stdin",
    )
    args = parser.parse_args()
    if args.demo:
        if args.input is not None:
            parser.error("currently demo mode only supports arguments, not -i")
        demo(args.text)
        sys.exit(0)

    if args.kind is None:
        import random

        random.seed()
        kind = random.choice(list(KINDS.values()))
    else:
        kind = args.kind
        if len(kind) > 1:
            kind = "".join(sorted(kind))
        if kind not in KINDS:
            parser.error("unknown kind {!r}".format(args.kind))
        else:
            kind = KINDS[kind]

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
