import urllib2

p = urllib2.urlopen("http://www.google.com")
print p
c = p.read()
# print c
print dir(p)
print p.headers.items()

# urllib2 automatically follos redirects. In most libraries this can be turned
# off.
p2 = urllib2.urlopen("http://www.example.com")
print p2.headers.items()

# Parsing XML
from xml.dom import minidom

xml_test = """<mytag>
        contents!
        <children>
            <item>1</item>
            <item>2</item>
        </children>
    </mytag>"""

x = minidom.parseString(xml_test)
print dir(x)
print x.toprettyxml()
print x.getElementsByTagName("mytag")
print x.getElementsByTagName("item")
print x.getElementsByTagName("item")[0]
print x.getElementsByTagName("item")[0].childNodes
print x.getElementsByTagName("item")[0].childNodes[0].nodeValue


# JSON
# Can express the same things XML can, but it is less verbose (because it has
# no tags). It exists of dictionaries and lists.

# Pasing JSON
import json
j = '{"one": 1, "numbers": [1, 2, 3.5]}'
d = json.loads(j)
print d
print d['numbers']
print d['one']
print d.keys()
print eval(j)
