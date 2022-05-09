import sys

args = sys.argv[1:]
idx = int(args[0]) - 40

myRegexLst = [
    r"/^[x.o]{64}$/i",
    r"/^[xo]*\.[xo]*$/i",
    r"/^\.|\.$|^x+o*\.|\.o*x+$/i",
    r"/^.(..)*$/s",
    r"/^(0|1[01])([01]{2})*$/s",
    r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
    r"/^(1?0+)*1*$/s",
    r"/^[bc]+$|^[bc]*a[bc]*$/s",
    r"/^[bc]+$|^(([bc]*a){2}[bc]*)+$/s",
    r"/^2(([02]*1){2}[02]*)*[20]*$|^((1[02]*){2})+$/s"
]

if idx < len(myRegexLst):
    print(myRegexLst[idx])
"""
IMPORTANT: On problem 48 it is possible to submit regular expressions that will time out the grader, which can lead to your account getting locked out.  The best way to prevent this is to verify, EACH TIME you change your problem 48 regex, that it fails (ie. does not match) in a timely way on the following two strings:
bbcbbcccbbcbcbbccbccbccbbcccbabccbcbcbccccccccbcbbbccbccbcb
bccbbcbbccbcbbabcbcbcbcbbccccacccbcbbcbbccbcacccbbcbbccbbcb

Part 2 of the regular expressions sequence - basic intermediate level.  Most of the entries will want some basic use of parens, but no advanced usage.  Same type of entry as in RE Lab 1.  For ease of file management, It is recommended that you augment the list of regular expressions, rather than having a separate file.

Submission is a command line script which receives an integer in [40,49] and returns the corresponding regex, delimited between forward slashes, with any options trailing (eg. /hi mom/i)

Word problems are case insensitive by default, string problems are not.  The questions do not allow for advanced usage of parens - they may only be used for grouping.

In Q40-42, An Othello board is any string of length 64 made up of only the characters in "xX.Oo".  An Othello edge is any string of length 8 made up of only the charaters in "xX.Oo".  A hole means a period.

Q40: Write a regular expression that will match on an Othello board represented as a string.
Q41: Given a string of length 8, determine whether it could represent an Othello edge with exactly one hole.
Q42: Given an Othello edge as a string, determine whether there is a hole such that if X plays to the hole (assuming it could), it will be connected to one of the corners through X tokens.  
Specifically, this means that one of the ends must be a hole, or starting from an end there is a sequence of at least one x followed immediately by a sequence (possibly empty) of o, immediately followed by a hole.
Q43: Match on all strings of odd length.
Q44: Match on all odd length binary strings starting with 0, and on even length binary strings starting with 1.
Q45: Match all words having two adjacent vowels that differ.
Q46: Match on all binary strings which DON’T contain the substring 110.
Q47: Match on all non-empty strings over the alphabet {a, b, c} that contain at most one a.
Q48: Match on all non-empty strings over the alphabet {a, b, c} that contain an even number of a's.
Q49: Match on all positive, even, base 3 integer strings.
"""
