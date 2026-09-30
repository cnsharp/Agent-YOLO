#!/usr/bin/env python3
"""Generate the IntelliJ (.kt) and Visual Studio (.cs) YoloLinkPatterns from the
canonical source in link_patterns_source.py.

IntelliJ is the source of truth (latest fixes). The generated `.kt` reproduces
IntelliJ's patterns exactly; the generated `.cs` is synced to IntelliJ (gaining
any patterns/fixes VS was missing).

Usage:
    python3 gen_link_patterns.py --check     # print generated blocks, do not write
    python3 gen_link_patterns.py --write     # inject blocks between the markers
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))  # Agent YOLO/
sys.path.insert(0, HERE)
import link_patterns_source as S  # noqa: E402

KT_TARGET = os.path.join(
    REPO_ROOT, "YOLO-IntelliJ", "src", "main", "kotlin", "com", "cnsharp",
    "yolo", "panel", "YoloLinkPatterns.kt")
CS_TARGET = os.path.join(REPO_ROOT, "YOLO-VS", "Links", "YoloLinkPatterns.cs")

START = ">>> YOLO_LINK_PATTERNS_START >>>"
END = "<<< YOLO_LINK_PATTERNS_END <<<"


def gen_kt():
    out = []
    out.append('internal const val PROGRAMMING_EXT: String = "%s"' % S.EXT_BASE)
    out.append("")
    for kt_name, _cs_name, rx in S.PATTERNS:
        rxk = rx.replace("<<EXT>>", "$PROGRAMMING_EXT")
        out.append('internal val %s: Pattern = Pattern.compile("""%s""")'
                   % (kt_name, rxk))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def gen_cs():
    ext_union = S.EXT_BASE + "|" + S.EXT_VS_EXTRA
    out = []
    out.append("internal const int MaxMatchesPerLine = %d;" % S.MAX_MATCHES_PER_LINE)
    out.append("")
    out.append('internal const string ProgrammingExt = "%s";' % ext_union)
    out.append("")
    for _kt_name, cs_name, rx in S.PATTERNS:
        rxc = rx.replace("<<EXT>>", "{0}")
        # .NET's regex engine has no possessive quantifiers; downgrade to greedy.
        rxc = rxc.replace("?+", "?").replace("*+", "*").replace("++", "+")
        # C# verbatim strings escape " as "".
        rxc = rxc.replace('"', '""')
        out.append("internal static readonly Regex %s = new Regex(" % cs_name)
        out.append("    string.Format(CultureInfo.InvariantCulture,")
        out.append('        @"%s",' % rxc)
        out.append("        ProgrammingExt),")
        out.append("    RegexOptions.Compiled);")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def inject(path, block):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
    si = next(i for i, l in enumerate(lines) if START in l)
    ei = next(i for i, l in enumerate(lines) if END in l)
    new_lines = lines[:si + 1] + block.split("\n") + lines[ei:]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--write"
    kt = gen_kt()
    cs = gen_cs()
    if mode == "--check":
        print("===== IntelliJ (.kt) block =====")
        print(kt)
        print("===== Visual Studio (.cs) block =====")
        print(cs)
        return
    if mode == "--write":
        inject(KT_TARGET, kt)
        inject(CS_TARGET, cs)
        print("Injected generated blocks into:")
        print("  " + KT_TARGET)
        print("  " + CS_TARGET)
        return
    print("unknown mode %r (use --check or --write)" % mode, file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
