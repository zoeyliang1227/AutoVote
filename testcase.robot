*** Settings ***
Library         Chunyu.py
Library         lily.py
Library         Shanyu.py
Library         Shanyu2.py
Library         ro.py


*** Test Cases ***
LILY
    lily.taxation

SHANYU
    Shanyu.kenting

SHANYU
    Shanyu2.kenting

LINGO
    Lingo.kenting

YEH
    yeh.dance

MIAN
    ro.ro
