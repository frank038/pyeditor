# gui style
GUISTYLE="Fusion"
# font famity to use for the editor
FONTFAMILY="Monospace"
# font size for the editor
FONTSIZE=14
# editor background colour
EDITORBACKCOLOR="#eeeeee"
# editor background colour dark theme
DEDITORBACKCOLOR="#262A2D"
# colour of matched braces
MATCHEDBRACECOLOR="#ffff00"
# colour of matched braces dark theme
DMATCHEDBRACECOLOR="#888888"
# background colour or the selected text
SELECTIONBACKGROUNDCOLOR="#008000"
# background colour or the selected text dark theme
DSELECTIONBACKGROUNDCOLOR=SELECTIONBACKGROUNDCOLOR
# close automatically: " ' ( [ {
AUTOCLOSE=True
# amount of characters to show a list for autocompletation
AUTOCOMPLETITION_CHARS=3
# end of line mode: "unix" or "windows"
ENDOFLINE="unix"
# indentation using tab (instead of spaces): False or True
USETAB=False
# the width of the indentation
TABWIDTH=4
# caret foreground colour
CARETFORE="#ff0000ff"
# caret background colour
CARETBACK="#1f0000ff"
# caret foreground colour dark theme
DCARETFORE="#BABAFF"
# caret background colour dark theme
DCARETBACK="#222222"
#
CARETWIDTH=4
# margin background color
MARGINBACKGROUND="#D0D0D0"
# margin background color dark theme
DMARGINBACKGROUND="#444444"
# margin text colour
MARGINFOREGROUND="#888888"
# margin text colour dark theme
DMARGINFOREGROUND="#000000"
# limit the number of entries in the history
HISTORYLIMIT=10
# autocompletion after the . character separator
USEWORDAUTOCOMLETION=1
# the width of the dialogs
DIALOGWIDTH=600
# use dark theme (except the following): 0 no - 1 yes
DARKTHEME=0
# use custom colours: 0 no - 1 yes
CUSTOMCOLORS=1
########## python
### THEME COLOURS
# Default
PDEFAULT="#000000"
# Comment
PCOMMENT="#A52A2A"
# Number
PNUMBER="#0D8C0D"
# Double-quoted string
PDOUBLEQ="#7F007F"
# Single-quoted string
PSINGELQ=PDOUBLEQ
# Keyword
PKEYW="#00007f"
# Triple single-quoted string
PTRIPLESQ="#A66B00"
# Triple double-quoted string
PTRIPLEDQ=PTRIPLESQ
# Class name
PCLASSNAME="#0212E1"
# Function or method name
PFUNCTION="#0212E1"
# Operator
POPERATOR="#0716E1"
# Identifier
PIDENTIFIER="#000000"
# Comment block
PCOMMENTB="#CA870D"
# Unclosed string
PUNCLOSEDSTRING="ff0000"
# Highlighted identifier
PHIGHLIGHTED="ffffff"
# Decorator
PDECORATOR="#FFA500"
### DARK THEME COLOURS
# Default
PDDEFAULT="#C5C8C6"
# Comment
PDCOMMENT="#A52A2A"
# Number
PDNUMBER="#0FAC0F"
# Double-quoted string
PDDOUBLEQ="#FFA500"
# Single-quoted string
PDSINGELQ=PDDOUBLEQ
# Keyword
PDKEYW="#008000"
# Triple single-quoted string
PDTRIPLESQ="#08A8A5"
# Triple double-quoted string
PDTRIPLEDQ=PDTRIPLESQ
# Class name
PDCLASSNAME="#6C77FF"
# Function or method name
PDFUNCTION="#6C77FF"
# Operator
PDOPERATOR=PDDEFAULT
# Identifier
PDIDENTIFIER="#BFBFBF"
# Comment block
PDCOMMENTB="#969896"
# Unclosed string
PDUNCLOSEDSTRING="ff0000"
# Highlighted identifier
PDHIGHLIGHTED="ffffff"
# Decorator
PDDECORATOR="#FFA500"
############# bash
### default theme
# Default
BDEFAULT=PDEFAULT
# Error
BERROR="#ff0000"
# Comment
BCOMMENT=PCOMMENT
# Number
BNUMBER=PNUMBER
# Keyword
BKEYW=PKEYW
# Double-quoted string
BDOUBLEQ=PDOUBLEQ
# Single-quoted string
BSINGELQ=PSINGELQ
# Operator
BOPERATOR=POPERATOR
# Identifier
BIDENTIFIER=PIDENTIFIER
# Scalar
BSCALAR=PDECORATOR
# Parameter expansion
BPAREXP=PSINGELQ
# Backticks
BBACKTICK=PSINGELQ
# Here document delimiter
BHDOCDEL=PSINGELQ
# Single-quoted here document
BSQHEREDOC=PSINGELQ
### dark theme
# Default
BDDEFAULT=PDDEFAULT
# Error
BDERROR="#ff0000"
# Comment
BDCOMMENT=PDCOMMENT
# Number
BDNUMBER=PDNUMBER
# Keyword
BDKEYW=PDKEYW
# Double-quoted string
BDDOUBLEQ=PDDOUBLEQ
# Single-quoted string
BDSINGELQ=PDSINGELQ
# Operator
BDOPERATOR=PDOPERATOR
# Identifier
BDIDENTIFIER=PDIDENTIFIER
# Scalar
BDSCALAR=PDDECORATOR
# Parameter expansion
BDPAREXP=BDSINGELQ
# Backticks
BDBACKTICK=BDSINGELQ
# Here document delimiter
BDHDOCDEL=BDSINGELQ
# Single-quoted here document
BDSQHEREDOC=BDSINGELQ
############## javascript
### default theme
# Default
JDEFAULT=PDEFAULT
# C comment
# C++ comment
# JavaDoc style C comment
# JavaDoc style C++ comment
# Pre-processor C comment
# JavaDoc style pre-processor comment
JCOMMENT=PCOMMENT
# Number
JNUMBER=PNUMBER
# Keyword
# JavaDoc keyword
JKEYW=PKEYW
# Double-quoted string
JDOUBLEQ=PDOUBLEQ
# Single-quoted string
JSINGELQ=PDOUBLEQ
# IDL UUID
JUUID=JSINGELQ
# Pre-processor block
JPREPB=JSINGELQ
# Operator
JOPERATOR=POPERATOR
# Identifier
JIDENTIFIER=PIDENTIFIER
# Unclosed string
JUNCLOSEDS=PUNCLOSEDSTRING
# C# verbatim string
JCVERBS=JDEFAULT
# Regular expression
JREGESPR=JDEFAULT
# Secondary keywords and identifiers
JSECKI=JIDENTIFIER
# JavaDoc keyword error
JJAVADOCERROR="#ff0000"
# Global classes and typedefs
JCLASSES=PCLASSNAME
# C++ raw string
JCPPRAWS=JDEFAULT
# Vala triple-quoted verbatim string
JVALATRQS=JDEFAULT
# Pike hash-quoted string
JPIKEHQS=JSINGELQ
# User-defined literal
JUSERDLIT=JDEFAULT
# Task marker
JTASKMARKER="#00ff00"
# Escape sequence
JESCAPES="#ff0000"
### dark theme
# Default
JDDEFAULT=PDDEFAULT
# C comment
# C++ comment
# JavaDoc style C comment
# JavaDoc style C++ comment
# Pre-processor C comment
# JavaDoc style pre-processor comment
JDCOMMENT=PDCOMMENT
# Number
JDNUMBER=PDNUMBER
# Keyword
# JavaDoc keyword
JDKEYW=PDKEYW
# Double-quoted string
JDDOUBLEQ=PDDOUBLEQ
# Single-quoted string
JDSINGELQ=PDDOUBLEQ
# IDL UUID
JDUUID=JDSINGELQ
# Pre-processor block
JDPREPB=JDSINGELQ
# Operator
JDOPERATOR=PDOPERATOR
# Identifier
JDIDENTIFIER=PDIDENTIFIER
# Unclosed string
JDUNCLOSEDS=PDUNCLOSEDSTRING
# C# verbatim string
JDCVERBS=JDDEFAULT
# Regular expression
JDREGESPR=JDDEFAULT
# Secondary keywords and identifiers
JDSECKI=JDIDENTIFIER
# JavaDoc keyword error
JDJAVADOCERROR="#ff0000"
# Global classes and typedefs
JDCLASSES=PDCLASSNAME
# C++ raw string
JDCPPRAWS=JDDEFAULT
# Vala triple-quoted verbatim string
JDVALATRQS=JDDEFAULT
# Pike hash-quoted string
JDPIKEHQS=JDSINGELQ
# User-defined literal
JDUSERDLIT=JDDEFAULT
# Task marker
JDTASKMARKER="#00ff00"
# Escape sequence
JDESCAPES="#ff0000"
########## text
### default theme
# text colour
TDEFAULT="#000000"
### dark theme
# text colour
TDDEFAULT="#C5C8C6"
