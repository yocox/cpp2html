#!/usr/bin/python

import sys
import re
import math
import hashlib
import colorsys

UNKNOWN, KEYWORD, ID, NUMBER, OP, PARAN, PP, COMMENT, SPACE = range(9)

#print 'yoco c++ highlight'

cppkw = '''alignas alignof asm auto bool break case catch char char16_t
char32_t class compl const constexpr const_cast continue decltype default
delete double dynamic_cast else enum explicit export extern false float for
friend goto if inline int long mutable namespace new noexcept nullptr operator
private protected public register reinterpret_cast return short signed sizeof
static static_assert static_cast struct switch template this thread_local throw
true try typedef typeid typename union unsigned using virtual void volatile
wchar_t while'''

kw = [k.strip() for k in cppkw.split()]

remm = '^/\*.*?\*/'
recm = '^//.*'
rekw = '^(' + '|'.join(kw) + ')(?!\w)'
renu = '^\d*\.\d+(?!\d)|^\d+(?!\d)'
recn = '^[A-Z_][A-Z0-9_]*(?!\w)'
reid = '^[a-zA-Z_]\w*(?!\w)'
repp = '^#.*'
repn = '^[(){}\[\]]+'
reop = '^[~!%^&*\-\+|:;,.<>/=?]+'
rest = r'^"(\\.|[^"])*?"'
rech = "^'.'"
resp = '^[ \t\n]+'

res = [ [recm, "comment"     , "666666"],
        [rekw, "keyword"     , "ffffb6"],
        [recn, "const"       , "99cc99"],
        [reid, "id"          , "f6f3e8"],
        [renu, "number"      , "ff73fd"],
        [repp, "preprocessor", "96cbfe"],
        [repn, "parenthes"   , "88bb33"],
        [reop, "operator"    , "cc0000"],
        [rest, "string"      , "a8ff60"],
        #[rech, "charator"    , "00cc00"],
        [rech, "charator"    , "ee8964"],
        [resp, "space"       , "444444"],
      ]

#print kw

class token :
    def __init__(self, t_, str_, color_) :
        self.t = t_
        self.string = str_
        self.color = color_

def getToken(s) :
    m = re.search(remm, s, re.DOTALL)
    if m != None :
        #print 'Matching! remm', m.group(0)
        return token('remm', m.group(0), '666666')
    for i in res :
        #print 'Trying ', i
        m = re.search(i[0], s)
        if m != None :
            #print 'Matching! %30s %30s' % (i[1], m.group(0))
            return token(i[1], m.group(0), i[2])
    return None

def parse(s) :
    tokens = []
    while True :
        t = getToken(s)
        if t == None :
            #print 'EEEEEEEEEEEEEEENNNNNNNNNNNNNNNNNNDDDDDDDDDDDDDDDD'
            break
        s = s[len(t.string):]
        tokens.append(t)
        #print 's ========%s==========' % s
    return tokens

def encode_html(s) :
    result = ''
    for c in s :
        if c == '\n' :
            result += '</li>\n<li>'
        elif c == '<' :
            result += '&lt;'
        elif c == '>' :
            result += '&gt;'
        elif c == '&' :
            result += '&amp;'
        elif c == ' ' :
            result += '&nbsp;'
        elif c == '"' :
            result += '&quot;'
        else :
            result += c
    return result

def linenumber(s) :
    lines = s.split('\n')
    result = ''
    logn = int( math.ceil(math.log(len(lines) - 1, 10)) )
    for i in range(0, len(lines) - 1) :
        result += '<font color="#666666">' + encode_html('%*d ' % (logn, i)) + '</font><br>\n'
    return result

hexstr = '0123456789abcdef'

def h(n) :
    return hexstr[int(n / 16)] + hexstr[n % 16]
    

def id_color(t) :
    if t.t != 'id' :
        return t.color
    else :
        hue = int(hashlib.sha1(t.string.encode()).hexdigest()[:2], 16) / 256.0
        print(t.string, hue)
        stu = 0.7
        light = 0.8
        rgb = colorsys.hls_to_rgb(hue, light, stu)
        rgb = [int(i * 256) for i in rgb]
        color = h(rgb[0]) + h(rgb[1]) + h(rgb[2])
        return color

def tohtml(tokens) :
    result = '<div style="background-color:#000000;color:#444;"><font face="monospace">\n<ol><li>'
    source_block = ''
    for t in tokens :
        html_str = encode_html(t.string)
        if t.t != 'space' :
            token_html = '<font color="' + id_color(t) + '">' + html_str + "</font>"
            if t.t == 'keyword' :
                token_html = '<b>' + token_html + '</b>'
            source_block += token_html
        else :
            source_block += html_str

    result += source_block

    result += '</li></ol></div>'
    return result

def hi(f) :
    s = open(f).read()
    #print s
    tokens = parse(s)
    html = tohtml(tokens)
    #print html
    f = open(f + '.html', 'w')
    f.write(html)
    f.close()

if __name__ == '__main__' :
    if len(sys.argv) == 1 :
        #print 'No input file'
        quit()
    for f in sys.argv[1:] :
        hi(f)

