import sys; args = sys.argv[1:]
idx = int(args[0]) - 71

myRegexLst = \
    [
        r'/^(?=(.)+(.*\1){3}).{,6}$/m',
        r'/^(?=(.*([aeiou])(?!.*\2)){5}).{,8}$/m',
        r'/(?=([^aeiou]*[aeiou][^aeiou]*){5}\b)^\w{17,}$/im',
        r'/^(.)(.)(.).{4,}\3\2\1$/im',
        r'/(?=.*(.)\1)^\w{22,}$/im',
        r'/(?=(.)+(.*\1){5,})\w{9,}$/im',
        r'/(?=((.)+\2){3})\w{14,}/',
        r'',
        r'',
        r'/(?!(.)+(.*\1){2})\w{18,}$/m'
    ]

if idx < len(myRegexLst):
    print(myRegexLst[idx])
# r'/(.)+(\w*\1){5,}\w*$/m',