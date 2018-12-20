import io
import urllib, urllib2, warnings
import httplib
import json
from socket import timeout
warnings.filterwarnings("ignore", category=UserWarning, module='urllib2')

class KODI_WEBSERVER:
    
    ip_port = ""
    
    def __init__(self, helper, _ConfigDefault, draw_default):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault
        self.draw_default = draw_default
        
        self.ip_port = 'http://'
        self.ip_port = self.ip_port+self._ConfigDefault['KODI.webserver.host']+':'+self._ConfigDefault['KODI.webserver.port']+'/'
        
        if self._ConfigDefault['KODI.webserver.user']!="" and self._ConfigDefault['KODI.webserver.pass']!="":
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, self.ip_port, self._ConfigDefault['KODI.webserver.user'], self._ConfigDefault['KODI.webserver.pass'])
            urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
        
    def getJSON(self, jsondata, get_parameter = 'jsonrpc?request='):
        self.draw_default.setInfoText("", self._ConfigDefault['color.white'])
        try:
            headers = {'content-type': 'application/json'}
            json_data = json.dumps(json.loads(jsondata))
            post_data = json_data.encode('utf-8')
            request = urllib2.Request(self.ip_port + get_parameter, post_data, headers)
            
            result = urllib2.urlopen(request,timeout=3).read()
            return json.loads(result.decode("utf-8"))
        except (IOError, httplib.HTTPException, timeout):
            self.draw_default.setInfoText("NO KODI ACCESS!", self._ConfigDefault['color.red'])
            return json.loads('{"id":1,"jsonrpc":"2.0","result":[]}')
        except:
            self.draw_default.setInfoText("NO KODI ACCESS!", self._ConfigDefault['color.red'])
            return json.loads('{"id":1,"jsonrpc":"2.0","result":[]}')
            
    def KODI_GetActivePlayers(self):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}')
            try:
                return parsed_json['result'][0]['playerid'], parsed_json['result'][0]['type']
            except KeyError:
                return 0, ""
            except IndexError:
                return 0, ""
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return ""

    def setPosterPath(self, playerid, poster_url, config):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Textures.GetTextures", "params": {  "properties":["cachedurl"] , "filter": {"field": "url", "operator": "is", "value":"' + urllib.unquote(poster_url) + '"}},"id": "'+str(playerid)+'"}')
	    config['poster_path'] = parsed_json['result']['textures'][0]['cachedurl']
        except KeyError:
	    print config['poster_path']
            config['poster_path'] = ''
        except IndexError:
            print config['poster_path']
            config['poster_path'] = ''
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            config['poster_path'] = ''
	except:
            print config['poster_path']
	    config['poster_path'] = ''

    def KODI_GetItem(self, playerid, playertype, config):
        try:
            if playertype == "video":
                player_params_id = "VideoGetItem"
            elif playertype == "audio":
                player_params_id = "AudioGetItem"
            else:
                return ""

            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "art"], "playerid": '+str(playerid)+' }, "id": "'+str(player_params_id)+'"}')
            try:
                title = parsed_json['result']['item']['title']
                if title=="":
                    title = parsed_json['result']['item']['label']

                if parsed_json['result']['item']['type'] == "episode":
                        poster_url = parsed_json['result']['item']['art']['tvshow.poster'][8:-1]
                elif parsed_json['result']['item']['type'] == "movie":
                        poster_url = parsed_json['result']['item']['art']['poster'][8:-1]
                elif parsed_json['result']['item']['type'] == "song":
                        poster_url = parsed_json['result']['item']['art']['album.thumb'][8:-1]
                else:
			poster_url = ""
			config['poster_path'] = ""

		if (poster_url != "" and poster_url != config['poster_url']):
			config['poster_url'] = poster_url
			self.setPosterPath(playerid, poster_url, config)

                return title
            except KeyError:
		poster_path = ""
                config['poster_path'] = ""
                return ""
            except IndexError:
		poster_path = ""
                config['poster_path'] = ""
                return ""
        except ValueError:
	    poster_path = ""
            config['poster_path'] = ""
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return ""
	except:
            poster_path = ""
            config['poster_path'] = ""
            return ""
        
    def KODI_GetProperties(self, playerid):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["speed","time","totaltime"] }, "id": 1}')
            try:
                speed = parsed_json['result']['speed']
                media_time = [int(parsed_json['result']['time']['hours']),int(parsed_json['result']['time']['minutes']),int(parsed_json['result']['time']['seconds'])]
                media_timetotal = [int(parsed_json['result']['totaltime']['hours']),int(parsed_json['result']['totaltime']['minutes']),int(parsed_json['result']['totaltime']['seconds'])]
                return speed, media_time, media_timetotal
            except KeyError, e:
                print "KeyError: " + str(e)
                return 0,[0,0,0],[0,0,0]
            except IndexError, e:
                print "IndexError: " + str(e)
                return 0,[0,0,0],[0,0,0]
        
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return 0,[0,0,0],[0,0,0]
        except:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return 0,[0,0,0],[0,0,0]
