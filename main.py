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

print("Addon_HANDLe:"+str(addon_handle))

xbmcplugin.setContent(addon_handle, 'songs')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def addLink(addon_handle, stationid, name, url, favicon, bitrate):
    li = xbmcgui.ListItem(name, iconImage=favicon)
    li.setInfo(type="Music", infoLabels={ "Title":name, "Size":bitrate})
    localUrl = build_url({'mode': 'play', 'stationid': stationid})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=localUrl, listitem=li)

def downloadFile(uri):
    req = urllib2.Request(uri)
    req.add_header('User-Agent', 'KodiRadioBrowser/1.0')
    response = urllib2.urlopen(req)
    data=response.read().decode('utf-8')
    # print(data)
    response.close()
    return data

mode = args.get('mode', None)

if mode is None:
    localUrl = build_url({'mode': 'stations', 'url': 'http://www.radio-browser.info/webservice/json/stations/topclick/100'})
    li = xbmcgui.ListItem('Top 100 Stations', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=localUrl, listitem=li, isFolder=True)

    localUrl = build_url({'mode': 'stations', 'url': 'http://www.radio-browser.info/webservice/json/stations/topvote/100'})
    li = xbmcgui.ListItem('Top 100 Voted Stations', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=localUrl, listitem=li, isFolder=True)

    localUrl = build_url({'mode': 'tags'})
    li = xbmcgui.ListItem('Tags', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=localUrl, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'tags':
    data = downloadFile('http://www.radio-browser.info/webservice/json/tags')
    dataDecoded = json.loads(data)
    for tag in dataDecoded:
        tagName = tag['name']
        if tag['stationcount'] > 1:
            try:
                localUrl = build_url({'mode': 'stations', 'url': 'http://www.radio-browser.info/webservice/json/stations/bytagexact/'+tagName})
                li = xbmcgui.ListItem(tagName, iconImage='DefaultFolder.png')
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=localUrl, listitem=li, isFolder=True)
            except:
                # print(tagName)
                # print('ignored tag:'+tagName)
                pass

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'stations':
    uri = args['url'][0]

    data = downloadFile(uri)
    dataDecoded = json.loads(data)
    for station in dataDecoded:
        addLink(addon_handle, station['id'], station['name'], station['url'], station['favicon'], station['bitrate'])
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'play':
    stationid = args['stationid'][0]
    data = downloadFile('http://www.radio-browser.info/webservice/v2/json/url/'+str(stationid))
    dataDecoded = json.loads(data)
    uri = dataDecoded['url']
    xbmc.Player().play(uri)
