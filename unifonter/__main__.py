#!/usr/bin/python3

import argparse
import itertools
import re
import sys
import unicodedata

_KINDS = {
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

_STYLES = {
    "b": "bold",
    "c": "script",
    "d": "double-struck",
    "f": "fraktur",
    "i": "italic",
    "k": "small-caps",
    "m": "monospace",
    "s": "sans-serif",
    "w": "fullwidth",
}

_EXCEPTIONS = {
    "FULLWIDTH SPACE": "IDEOGRAPHIC SPACE",
    "MATHEMATICAL SCRIPT SMALL E": "SCRIPT SMALL E",
    "MATHEMATICAL SCRIPT SMALL O": "SCRIPT SMALL O",
    "MATHEMATICAL SCRIPT SMALL G": "SCRIPT SMALL G",
    "MATHEMATICAL SCRIPT CAPITAL B": "SCRIPT CAPITAL B",
    "MATHEMATICAL SCRIPT CAPITAL E": "SCRIPT CAPITAL E",
    "MATHEMATICAL SCRIPT CAPITAL F": "SCRIPT CAPITAL F",
    "MATHEMATICAL SCRIPT CAPITAL H": "SCRIPT CAPITAL H",
    "MATHEMATICAL SCRIPT CAPITAL I": "SCRIPT CAPITAL I",
    "MATHEMATICAL SCRIPT CAPITAL L": "SCRIPT CAPITAL L",
    "MATHEMATICAL SCRIPT CAPITAL M": "SCRIPT CAPITAL M",
    "MATHEMATICAL SCRIPT CAPITAL R": "SCRIPT CAPITAL R",
    "MATHEMATICAL FRAKTUR CAPITAL C": "BLACK-LETTER CAPITAL C",
    "MATHEMATICAL FRAKTUR CAPITAL H": "BLACK-LETTER CAPITAL H",
    "MATHEMATICAL FRAKTUR CAPITAL I": "BLACK-LETTER CAPITAL I",
    "MATHEMATICAL FRAKTUR CAPITAL R": "BLACK-LETTER CAPITAL R",
    "MATHEMATICAL FRAKTUR CAPITAL Z": "BLACK-LETTER CAPITAL Z",
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL C": "DOUBLE-STRUCK CAPITAL C",
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL H": "DOUBLE-STRUCK CAPITAL H",
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL N": "DOUBLE-STRUCK CAPITAL N",
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL P": "DOUBLE-STRUCK CAPITAL P",
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL Q": "DOUBLE-STRUCK CAPITAL Q",
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL R": "DOUBLE-STRUCK CAPITAL R",
    "MATHEMATICAL DOUBLE-STRUCK CAPITAL Z": "DOUBLE-STRUCK CAPITAL Z",
    "MATHEMATICAL ITALIC SMALL H": "PLANCK CONSTANT",
    #    "LATIN LETTER SMALL CAPITAL Q": "LATIN SMALL LETTER O WITH OGONEK",
}

rx = re.compile(r"^LATIN (\S+) LETTER (\S+)$")


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
                        name = rx.sub(lrepl, name)
                if name in _EXCEPTIONS:
                    name = _EXCEPTIONS[name]
                s.append(unicodedata.lookup(name))
            except (ValueError, KeyError):
                s.append(l)
    return "".join(s)


def demo(text):
    if len(text) == 0:
        print(" USE  TO GET")
        for k in _KINDS:
            print(" %3s  %s" % (k, unifonter(_KINDS[k].title(), _KINDS[k])))
    else:
        for k in _KINDS:
            print(unifonter(" ".join(text), _KINDS[k]))


if __name__ == "__main__":
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
        + ", ".join(
            "%s (%s)" % (k, unifonter(v, _KINDS[k])) for (k, v) in _STYLES.items()
        )
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
        kind = random.choice(list(_KINDS.values()))
    else:
        kind = args.kind
        if len(kind) > 1:
            kind = "".join(sorted(kind))
        if kind not in _KINDS:
            parser.error("unknown kind {!r}".format(args.kind))
        else:
            kind = _KINDS[kind]

    if len(args.text) == 0:
        if args.input is not None:
            it = args.input
        else:
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
