#coding:utf-8
from __future__ import print_function
import re,codecs,opencc



repl = re.compile('"(.*?)"\s*=\s*"(.*?)"')
with codecs.open('zh-Hans.lproj/Localizable.strings', 'r', encoding='utf-8') as f:
    with codecs.open('zh-Hant.lproj/Localizable.strings', 'w', encoding='utf-8') as fw:
	for line in f.readlines():
	    result = repl.match(line)
	    if result:
		key = result.group(1)
		value = result.group(2) 
	 	fw.write('"'+key+'" = "'+opencc.convert(value, config='s2t.json')+'";')
	    else:
		fw.write(line)


