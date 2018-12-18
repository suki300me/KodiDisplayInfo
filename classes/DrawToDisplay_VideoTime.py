import io
from datetime import timedelta
try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

class DrawToDisplay_VideoTime:
    
    # default for 320x240
    _drawSetting = {}   
    _drawSetting['videoinfo.progressbar.margin_top'] = 85
    _drawSetting['videoinfo.progressbar.height'] = 25
    
    _drawSetting['videoinfo.button.play'] = ""
    _drawSetting['videoinfo.button.break'] = ""
    
    _drawSetting['videoinfo.title.fontsize'] = 43
    _drawSetting['videoinfo.title.height_margin'] = 4
    _drawSetting['videoinfo.title.margin_left'] = 230
    
    _drawSetting['videoinfo.time_now.fontsize'] = 60
    _drawSetting['videoinfo.time_now.height_margin'] = 68
    _drawSetting['videoinfo.time_end.fontsize'] = 60
    _drawSetting['videoinfo.time_end.height_margin'] = 68
    
    _drawSetting['videoinfo.time.fontsize'] = 64
    _drawSetting['videoinfo.time.margin_left'] = 0
    _drawSetting['videoinfo.time.margin_top'] = 67
    
    _drawSetting['videoinfo.length.fontsize'] = 30

    # in seconds
    time = 0
    totaltime = 0
    
    def __init__(self, helper, _ConfigDefault):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault
        
    def setPygameScreen(self, pygame, screen, draw_default):
        self.pygame = pygame
        self.screen = screen
        self.draw_default = draw_default
        
        getattr(self, 'SetupDrawSetting'+self._ConfigDefault['display.resolution'])()
    
    def SetupDrawSetting320x240(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_320x240.png')
        
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_320x240.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_320x240.png')
	self._drawSetting['videoinfo.default_poster'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/poster_320x240.png')
    
    def SetupDrawSetting480x272(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x272.png')
        self._drawSetting['startscreen.clock.fontsize'] = 64
        self._drawSetting['startscreen.clock.height_margin'] = 102
        
        self._drawSetting['videoinfo.progressbar.margin_top'] = 92
        self._drawSetting['videoinfo.progressbar.height'] = 34
        
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')
    
        self._drawSetting['videoinfo.title.fontsize'] = 60
        self._drawSetting['videoinfo.title.height_margin'] = 5
	self._drawSetting['videoinfo.title.margin_left'] = 230
    
        self._drawSetting['videoinfo.time_now.fontsize'] = 80
        self._drawSetting['videoinfo.time_now.height_margin'] = 86
        self._drawSetting['videoinfo.time_end.fontsize'] = 80
        self._drawSetting['videoinfo.time_end.height_margin'] = 86
        
        self._drawSetting['videoinfo.time.fontsize'] = 81
        self._drawSetting['videoinfo.time.margin_left'] = 14
        self._drawSetting['videoinfo.time.margin_top'] = 83

	self._drawSetting['videoinfo.length.fontsize'] = 30
	self._drawSetting['videoinfo.default_poster'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/poster_480x320.png')

    def SetupDrawSetting480x320(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x320.png')
        self._drawSetting['startscreen.clock.fontsize'] = 75
        self._drawSetting['startscreen.clock.height_margin'] = 118
        
        self._drawSetting['videoinfo.progressbar.margin_top'] = 146
        self._drawSetting['videoinfo.progressbar.height'] = 10
        
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')
     
        self._drawSetting['videoinfo.title.fontsize'] = 60
        self._drawSetting['videoinfo.title.height_margin'] = 0
	self._drawSetting['videoinfo.title.margin_left'] = 230
    
        self._drawSetting['videoinfo.time_now.fontsize'] = 70
        self._drawSetting['videoinfo.time_now.height_margin'] = 76
        self._drawSetting['videoinfo.time_end.fontsize'] = 42
        self._drawSetting['videoinfo.time_end.height_margin'] = 38
        
        self._drawSetting['videoinfo.time.fontsize'] = 42
        self._drawSetting['videoinfo.time.margin_left'] = 230
        self._drawSetting['videoinfo.time.margin_top'] = 66

	self._drawSetting['videoinfo.length.fontsize'] = 26
	self._drawSetting['videoinfo.default_poster'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/poster_480x320.png')

        
    def drawProgressBar(self, margin_top = 0):
        rect_bar = self.pygame.Rect((230,self._drawSetting['videoinfo.progressbar.margin_top']+margin_top), (self.screen.get_width()-230,self._drawSetting['videoinfo.progressbar.height']))
        
        if self.totaltime > 0:
            percent_done = int(( 1. * rect_bar.width / self.totaltime) * self.time)
        else:
            percent_done = 0
          
        rect_done = self.pygame.Rect(rect_bar)
        rect_done.width = percent_done
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.green'], rect_bar)
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.orange'], rect_done)
        self.pygame.draw.rect(self.screen, 000000, rect_bar, 1)
        
    def drawProperties(self, video_title, time_now, speed, media_time, media_totaltime, poster):
        margin_top = 0
        videoinfo_title_fontsize = self._drawSetting['videoinfo.title.fontsize']
        
        self.time = self.helper.format_to_seconds(media_time[0], media_time[1], media_time[2])
        self.totaltime = self.helper.format_to_seconds(media_totaltime[0], media_totaltime[1], media_totaltime[2])
        
        if len(video_title)>15 and self._ConfigDefault['config.titleformat']=="twoline":                    
            max_word_count = 21
            if self._ConfigDefault['display.resolution']=="480x320":
                videoinfo_title_fontsize = 49
                margin_top = -18
                second_title_height_margin = -46
		poster_height = 320
		poster_width = 220
            if self._ConfigDefault['display.resolution']=="480x272":
                videoinfo_title_fontsize = 42
                margin_top = -11
                second_title_height_margin = -40
                poster_height = 320
                poster_width = 220
            if self._ConfigDefault['display.resolution']=="320x240":
                videoinfo_title_fontsize = 40
                margin_top = -16
                max_word_count = 16
                second_title_height_margin = -38
                poster_height = 240
                poster_width = 165
                
            last_space = video_title.rindex(' ', 0, max_word_count);
            old_video_title = video_title
            line1 = old_video_title[0:last_space].strip()
            line2 = old_video_title[last_space:].strip()
      
            self.draw_default.displaytext(line1, videoinfo_title_fontsize, self._drawSetting['videoinfo.title.margin_left'], self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin']+second_title_height_margin, 'left', (self._ConfigDefault['color.white']))
            self.draw_default.displaytext(line2, videoinfo_title_fontsize, self._drawSetting['videoinfo.title.margin_left'], self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
        else:
	    if len(video_title)>7:
		videoinfo_title_fontsize=40
            self.draw_default.displaytext(video_title, videoinfo_title_fontsize, self._drawSetting['videoinfo.title.margin_left'], self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
        
        self.draw_default.displaytext(str(time_now.strftime("%-I:%M%p")), self._drawSetting['videoinfo.time_now.fontsize'], self.screen.get_width(), self._drawSetting['videoinfo.time_now.height_margin'], 'right', (self._ConfigDefault['color.white']))

       
        addtonow = time_now + timedelta(seconds=(self.totaltime-self.time))
        self.draw_default.displaytext(str('Ends: ' + addtonow.strftime("%-I:%M%p")), self._drawSetting['videoinfo.time_end.fontsize'], self.screen.get_width(), self._drawSetting['videoinfo.time_now.height_margin'] + self._drawSetting['videoinfo.time_end.height_margin'], 'right', (self._ConfigDefault['color.white']))
    
        margin_progessbar = self._drawSetting['videoinfo.progressbar.margin_top']+self._drawSetting['videoinfo.progressbar.height']+margin_top

        if self._ConfigDefault['config.timeformat']=="minutes":
            self.draw_default.displaytext(str(self.helper.format_to_minutes(media_time[0], media_time[1])), self._drawSetting['videoinfo.time.fontsize'], 62+self._drawSetting['videoinfo.time.margin_left'], margin_progessbar+self._drawSetting['videoinfo.time.margin_top'], 'left', (self._ConfigDefault['color.white']))
            self.draw_default.displaytext(str(self.helper.format_to_minutes(media_totaltime[0], media_totaltime[1])), self._drawSetting['videoinfo.time.fontsize'], self.screen.get_width()-10, margin_progessbar+self._drawSetting['videoinfo.time.margin_top'], 'right', (self._ConfigDefault['color.white']))  
        elif self._ConfigDefault['config.timeformat']=="kodi":
            fontsize = 53
            margintop = 15
            if self._ConfigDefault['display.resolution']=="320x240":
                margintop = 16
            
            self.draw_default.displaytext(self.helper.format_to_string(media_time[0], media_time[1], media_time[2]), self._drawSetting['videoinfo.time.fontsize'], self.screen.get_width(), margin_progessbar+self._drawSetting['videoinfo.time.margin_top']-margintop, 'right', (self._ConfigDefault['color.white']))
            self.draw_default.displaytext('Length: '+self.helper.format_to_string(media_totaltime[0], media_totaltime[1], media_totaltime[2]), self._drawSetting['videoinfo.length.fontsize'], self.screen.get_width(), margin_progessbar+self._drawSetting['videoinfo.time.margin_top']-margintop+26, 'right', (self._ConfigDefault['color.white']))  
               
        self.drawProgressBar(margin_top)
                
        if speed == 1:
            self.screen.blit(self._drawSetting['videoinfo.button.play'], (230, margin_progessbar+8))
        else:
            self.screen.blit(self._drawSetting['videoinfo.button.break'], (230, margin_progessbar+8))

	try:
	    if poster == "":
		self.screen.blit(self._drawSetting['videoinfo.default_poster'], (0, 0))
	    else:
	    	scaled_poster = self.pygame.transform.scale(self.pygame.image.load(io.BytesIO(poster)), (poster_width, poster_height))
            	self.screen.blit(scaled_poster, (0, 0))
	except:
            self.screen.blit(self._drawSetting['videoinfo.default_poster'], (0, 0))

