import sys
import urllib
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
import json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def addLink(name, url, favicon):
    li = xbmcgui.ListItem(name, iconImage=favicon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

def downloadFile(uri):
    req = urllib2.Request(uri)
    req.add_header('User-Agent', 'KodiRadioBrowser/1.0')
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    return data

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'folder', 'foldername': 'topclick', 'url': 'http://www.radio-browser.info/webservice/json/stations/topclick/100'})
    li = xbmcgui.ListItem('Top 100 Stations', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'topvote', 'url': 'http://www.radio-browser.info/webservice/json/stations/topvote/100'})
    li = xbmcgui.ListItem('Top 100 Voted Stations', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    uri = args['url'][0]

    data = downloadFile(uri)
    dataDecoded = json.loads(data)
    for station in dataDecoded:
        print(station)
        addLink(station['name'], station['url'], station['favicon'])
    xbmcplugin.endOfDirectory(addon_handle)
