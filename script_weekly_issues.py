# -*- coding: utf-8 -*-
import json
import urllib2

try:
    req = urllib2.urlopen("https://api.github.com/repos/g0v/kuansim/issues")
    issues = req.read()

    json_issues = json.loads(issues)
    dict_labels = {}
    for x in json_issues:
        if x["labels"]:
            for y in x["labels"]:
                dict_labels[y["name"]] = y["name"]
    # print sorted(dict_labels)

    print "尚未認養:"
    for x in json_issues:
    	if not x["assignee"]:
    	    print "%s\t%s" % (x["number"], x["title"])

    print "\n";
    print "已認養:"
    for x in json_issues:
    	if x["assignee"]:
    	    print "%s\t%s %s %s" % (x["number"], x["title"], "->", x["assignee"]["login"])
    # print json_issues
except Exception, e:
	print "喔喔出錯囉...: %s" % (e.args)
else:
	pass
finally:
	pass