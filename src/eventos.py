import xml.etree.ElementTree as ET

'''
mapa = ET.parse('resources/network.xml')
mapa_root = mapa.getroot()

for i in mapa_root.findall('links/link'):
    print(i.get('id'))'''

planes = ET.parse('resources/plans.xml')
planes_root = planes.getroot()

for i in planes_root.findall('person'):
    print(i.get('id'))