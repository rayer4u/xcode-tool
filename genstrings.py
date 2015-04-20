#coding:utf-8
# Usage:
#
#   python localized.py > Localization.strings
#
# This script should be placed in the Xcode project folder. It will read all .m files 
# and extract all NSLocalizedString and Localized codes.
#
# Differences between this and genstrings from Apple tool:
# - Group the strings by the filename (instead of alphabetically)
# - Scan for "Localized" code, which is a Macro for NSLocalizedString with recursive replacement and optional comment
#
# This script is heavily copied from: https://github.com/dunkelstern/Cocoa-Localisation-Helper

from __future__ import print_function
import os, sys, re, subprocess, codecs, traceback


def fetch_files_recursive(directory, *extensions):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
	for filename in filenames:
	    for ext in extensions:
	        if filename.endswith(ext):
		    matches.append(os.path.join(root, filename))
		    break
    return matches
    

# prepare regexes
localizedStringComment = re.compile('NSLocalizedString\(@"(.*?)",\s*@"(.*?)"\s*\)', re.DOTALL)
localized = re.compile('I\(@"(.*?)"\)', re.DOTALL)

# get string list
uid = 0
strings = []
for file in fetch_files_recursive('.', '.m', '.mm', '.h'):
    with codecs.open(file, 'r', encoding='utf-8') as f:
        try:
	    content = f.read()
            for result in localizedStringComment.finditer(content):
                uid += 1
                strings.append((result.group(1), result.group(2), file, uid))
            for result in localized.finditer(content):
                uid += 1
                strings.append((result.group(1), '', file, uid))
	except:
	    #不是utf8的文件直接pass
	    print(file+' is not utf8,pass', file=sys.stderr)
	    traceback.print_exc(file=sys.stderr)

# find duplicates
duplicated = []
filestrings = {}
for string1 in strings:
    dupmatch = 0
    for string2 in strings:
        if string1[3] == string2[3]:
            continue
        if string1[0] == string2[0]:
            if string1[2] != string2[2]:
                dupmatch = 1
		#需要循环完
            	break
    if dupmatch == 1:
        dupmatch = 0
        for string2 in duplicated:
            if string1[0] == string2[0]:
                dupmatch = 1
                break
        if dupmatch == 0:
            duplicated.append(string1)
    else:
        dupmatch = 0 
        if string1[2] in filestrings:
            for fs in filestrings[string1[2]]:
                if fs[0] == string1[0]:
                    dupmatch = 1
                    break
        else:
            filestrings[string1[2]] = []
        if dupmatch == 0:
            filestrings[string1[2]].append(string1)

print('//This file is auto generate by genstring.py from project https://github.com/rayer4u/xcode-tool\n\n')
# output filewise
for key in filestrings.keys():
    print('/*\n * ' + key + '\n */\n')

    strings = filestrings[key]
    for string in strings:
        if string[1] != '':
	    print('/* ' + string[1] + ' */')
        print ('"' + string[0].encode('utf8') + '" = "' + string[0].encode('utf8') + '";')
        print('\n')
    print ('\n')


print('\n\n')
print('/*\n * SHARED STRINGS\n */\n')

# output duplicates
for string in duplicated:
    if string[1] != '':
        print('/* ' + string[1] + ' */')
    print ('"' + string[0].encode('utf8') + '" = "' + string[0].encode('utf8') + '";')
    print('\n')
