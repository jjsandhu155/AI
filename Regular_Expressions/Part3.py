import sys

args = sys.argv[1:]
idx = int(args[0]) - 50

myRegexLst = \
    [
        r"/^(?=(.)+(.*\1){3}).{,6}$/m", # 25
    r"/^(?=(.*([aeiou])(?!.*\2)){5}).{,8}$/m", # 35
    r"/^(?=([^aeiou]*[aeiou]){5}[^aeiou]*$).{18,}$/im", # 43, didn't need \n since $ anchors it
    r"/^(.)(.)(.).{2,}\3\2\1$/m", # 22 it's better not to do the reverse thinking way
    r"/(?=(.)+\1).{20,}$/m", # 17 requires at least two in a row, should work for general cases
    #r"/(?=(.)+(.*\1){5})\w*$/m", # 25 6 above
    r"/(.)+(\w*\1){5,}\w*$/m", # 19 yay
    r"/(?=((.)+\2){3})\w{14,}/", # 22
    "",
    "",
    r"/(?!(.)+(.*\1){2})\w{18,}$/m" # 25
    ]

if idx < len(myRegexLst):
    print(myRegexLst[idx])
