# Canonical link-detection RegExp source for Agent YOLO (SINGLE SOURCE OF TRUTH).
#
# Derived from the IntelliJ plugin's YoloLinkPatterns.kt (which is the source of truth
# per the Metadata-mgmt Spec and the latest fixes). Both the IntelliJ (.kt) and the
# Visual Studio (.cs) link-pattern files are GENERATED from this module so the regex
# bodies never drift between platforms.
#
# Placeholder convention:
#   <<EXT>>  -> the programming-extension allowlist (PROGRAMMING_EXT).
#               .kt emits it as the Kotlin interpolation "$PROGRAMMING_EXT";
#               .cs emits it as the string.Format arg "{0}" (and downgrades the
#               possessive quantifiers *+ / ?+ / ++ that .NET's regex engine lacks).
#
# The extension allowlist has two parts:
#   EXT_BASE      - the cross-language base (from IntelliJ) - shared by both platforms.
#   EXT_VS_EXTRA  - Visual Studio / C# / .NET-only extensions, kept as a platform delta
#                   (the Spec permits per-language differences).

# Cross-language base extension allowlist (IntelliJ source).
EXT_BASE = (
    "kt|kts|java|scala|sc|groovy|gradle|"
    "py|pyi|pyw|rb|rake|php|pl|pm|lua|sh|bash|zsh|ksh|bat|cmd|ps1|psm1|psd1|"
    "js|jsx|mjs|cjs|ts|tsx|vue|html|htm|xhtml|css|scss|sass|less|styl|"
    "go|rs|c|h|cc|cpp|cxx|hpp|hxx|hh|cs|m|mm|swift|d|nim|zig|s|asm|"
    "ex|exs|clj|cljs|cljc|erl|hs|ml|mli|fs|fsx|fsi|jl|r|proto|sol|graphql|gql|"
    "xml|xsd|xsl|xslt|wsdl|json|json5|jsonc|yaml|yml|toml|ini|cfg|conf|config|"
    "properties|env|lock|csv|tsv|log|"
    "md|markdown|rst|txt|text|diff|patch|editorconfig|gitignore|dockerignore|"
    "tf|tfvars|feature|bnf|avsc|edn|"
    "iml|ipr|iws"
)

# Visual Studio / C# / .NET-only extensions (platform delta, appended for the VS build).
# Covers the .NET-family languages IntelliJ's base list omits (VB, Razor, XAML, …)
# plus the usual .NET project / build / packaging / asset extensions.
EXT_VS_EXTRA = (
    # .NET languages & markup (not in EXT_BASE)
    "vb|razor|cshtml|vbhtml|xaml|csx|cake|aspx|ascx|ashx|asmx|asax|"
    # project / build files
    "csproj|vbproj|fsproj|sln|slnx|props|targets|vcxproj|vcxitems|user|"
    "ruleset|publishproj|vsix|nuspec|appxmanifest|"
    # packaging / asset / misc (file types the IDE can actually open — NO binaries like dll/exe)
    "manifest|resx|settings|dbml|edmx"
)

MAX_MATCHES_PER_LINE = 50

# (kt_name, cs_name, regex_with_placeholder)
# Order matters: the generator emits declarations in this sequence.
PATTERNS = [
    ("PATH_PATTERN", "PathPattern",
     r"""(?<![\\/\w.])((?:(?:[A-Za-z]:[\\/]?)|[\\/]|[~][\\/]?|\\\\[A-Za-z0-9._\-]+(?:[\\/][A-Za-z0-9._\-]+)+|[A-Za-z0-9._\-]+[\\/])(?:[A-Za-z0-9._\-]+[\\/])*(?:[A-Za-z0-9._\-]+\.((?i:<<EXT>>))(?![\\/\w.])|[A-Za-z0-9._\-]+))(?::(\d+)(?:-(\d+))?(?::(\d+))?)?"""),

    ("QUOTED_PATH_PATTERN", "QuotedPathPattern",
     r"""(["'])((?:[A-Za-z]:)?[\\/][^"']*?\.(?i:<<EXT>>))\1(?::(\d+))?(?::(\d+))?"""),

    ("STACK_BARE_PATTERN", "StackBarePattern",
     r"""(?<![\\/\w.\-])([\w.\-]+\.(?i:<<EXT>>)):(\d+)(?::(\d+))?"""),

    ("STACK_BARE_NAME_PATTERN", "StackBareNamePattern",
     r"""(?<![\\/\w.\-])([\w.\-]+\.(?i:<<EXT>>)|\.(?:gitignore|dockerignore|editorconfig))(?![\\/\w.:])"""),

    ("STACK_PY_DQ_PATTERN", "StackPyDqPattern",
     r"""File "([^"]+\.(?i:<<EXT>>))", line (\d+)"""),

    ("STACK_PY_SQ_PATTERN", "StackPySqPattern",
     r"""File '([^']+\.(?i:<<EXT>>))', line (\d+)"""),

    ("TYPE_NAME_PATTERN", "TypeNamePattern",
     r"""(?<![.\w/\\])(?<qualified>\\?(?:[A-Za-z_][A-Za-z0-9_]*+)(?:(?:\.|::|\\)[A-Za-z_][A-Za-z0-9_]*+)+)(?!\.[a-z])(?![#.][A-Za-z_]\w*)(?!:\d)"""
     r"""|(?<![.\w/\\])(?<simple>(?![A-Z]+\b)[A-Z][a-zA-Z0-9_]*+)(?!\.[a-z])(?![#.][A-Za-z_]\w*)(?!:\d)"""),

    ("TYPE_LINE_PATTERN", "TypeLinePattern",
     r"""(?<![.\w/\\])(?:(?<qualified>\\?(?:[A-Za-z_][A-Za-z0-9_]*+)(?:(?:\.|::|\\)[A-Za-z_][A-Za-z0-9_]*+)+)|(?<simple>(?![A-Z]+\b)[A-Z][a-zA-Z0-9_]*+)):(?<line>\d+)(?::(?<col>\d+))?"""),

    ("MEMBER_REF_PATTERN", "MemberRefPattern",
     r"""(?<class>(?<![.\w/\\])(?:\\?(?:[A-Za-z_][A-Za-z0-9_]*+)(?:(?:\.|::|\\)[A-Za-z_][A-Za-z0-9_]*+)+)|(?<![.\w/\\])[A-Z][a-zA-Z0-9_]*+)[.#](?<member>[A-Za-z_]\w*)"""),

    ("URL_PATTERN", "UrlPattern",
     r"""https?://[^\s<>"'\)\]]+"""),

    ("TYPE_HEAD_PATTERN", "TypeHeadPattern",
     r"""(?<![.\w/\\])(?<qualified>\\?(?:[A-Za-z_][A-Za-z0-9_]*+)(?:(?:\.|::|\\)[A-Za-z_][A-Za-z0-9_]*+)+)\s*$"""),

    ("BARE_HEAD_PATTERN", "BareHeadPattern",
     r"""(?<![\\/\w.\-])([A-Z][A-Za-z0-9_\-]{2,})\s*$"""),

    ("MEMBER_HEAD_PATTERN", "MemberHeadPattern",
     r"""(?<![.\w/\\])(?<class>(?:(?:\\?(?:[A-Za-z_][A-Za-z0-9_]*+)(?:(?:\.|::|\\)[A-Za-z_][A-Za-z0-9_]*+)+)|[A-Z][a-zA-Z0-9_]*+))\s*$"""),
]
