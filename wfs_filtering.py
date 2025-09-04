import urllib.request
import json

pandidentificatie = "0344100000135173" 
filter_xml = f'<Filter><PropertyIsEqualTo><PropertyName>identificatie</PropertyName><Literal>NL.IMBAG.Pand.{pandidentificatie}</Literal></PropertyIsEqualTo></Filter>'
filter_encoded = urllib.parse.quote(filter_xml)
url = (
    'https://data.3dbag.nl/api/BAG3D/wfs?'
    'request=getfeature&service=wfs&version=2.0.0&typenames=BAG3D:lod22'
    f'&filter={filter_encoded}&outputFormat=application/json'
)
print(url)
data = urllib.request.urlopen(url).read()
json_data = json.loads(data)
print(json_data)