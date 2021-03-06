'''
Created on 6 feb 2012

@author: Batch, kinkin
'''

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, gzip
import settings
from common import notification, get_url, regex_get_all, regex_from_to, create_directory, write_to_file, read_from_file, clean_file_name, get_file_size, wait, wait_dl_only
from datetime import date, timedelta
import urllib, os, sys, re, urllib2
import shutil, glob
from furk import FurkAPI
from mediahandler import play, download, download_and_play, set_resolved_url
from meta import TheTVDBInfo, set_movie_meta, download_movie_meta, set_tv_show_meta, download_tv_show_meta, meta_exist
from threading import Thread
from metahandler import metahandlers
metainfo = metahandlers.MetaData()
import time
import datetime
import zipfile
import sqlite3

ADDON = settings.addon()
ADDON.setSetting('disable_dialog', value='ENABLE')
DISABLE_DIALOG = settings.disable_dialog()
DATA_PATH = settings.data_path()
CACHE_PATH = settings.cache_path()
COOKIE_JAR = settings.cookie_jar()
SUBSCRIPTION_FILE = settings.subscription_file()
IMDB_SEARCH_FILE = settings.imdb_search_file()
IMDB_ACTOR_FILE = settings.imdb_actor_file()
FURK_SEARCH_FILE = settings.furk_search_file()
DUMMY_PATH = settings.dummy_path()
DOWNLOAD_PATH = settings.download_path()
META_PATH = settings.meta_path()
FURK_MODERATED = settings.furk_moderated()
#FURK_SHOW_FILE_SIZE = settings.furk_file_size()
#FURK_FILE_SIZE_UNIT = settings.furk_file_size_unit()
IMDB_TITLE_SEARCH = settings.imdb_search_url()
IMDB_ACTOR_SEARCH = settings.imdb_actors_url()
COUNT = settings.imdb_filter_count()
PRODUCTION_STATUS = settings.imdb_filter_status()
VIEW = settings.imdb_filter_view()
RELEASE_DATE = settings.imdb_filter_release()
USER_RATING = settings.imdb_filter_rating()
NUM_VOTES = settings.imdb_filter_votes()
IMDB_RESULTS = settings.imdb_results()
FURK_ACCOUNT = settings.furk_account()
FURK_USER = settings.furk_user()
FURK_PASS = settings.furk_pass()
SUBSCRIPTIONS_ACTIVATED = settings.subscription_update()
UNICODE_INDICATORS = settings.use_unicode()
DOWNLOAD_META = settings.download_meta()
MOVIES_PATH = settings.movies_directory()
TV_SHOWS_PATH = settings.tv_show_directory()
PLAY_MODE = settings.play_mode()
FURK = FurkAPI(COOKIE_JAR)
SORT_TOP_MOV = settings.top_movies_sort()
SORT_MOV_MPAA = settings.mpaa_sort()
SORT_MOV_GEN = settings.movie_genre_sort()
SORT_MOV_GRP = settings.movie_group_sort()
SORT_MOV_STU = settings.movie_studio_sort()
SORT_MOV_NEW = settings.new_movies_sort()
SORT_BLU_RAY = settings.blu_ray_sort()
SORT_TOP_TV = settings.top_tv_sort()
SORT_TV_GEN = settings.tv_genre_sort()
SORT_TV_GRP = settings.tv_group_sort()
SORT_TV_ACT = settings.tv_active_sort()
SORT_IMDB_SEARCH = settings.imdb_search_sort()
XBMC_SORT = settings.xbmc_sort()
NEWMOVIE_DAYS = settings.newmovie_days()
CUSTOMQUALITY = settings.custom_quality()
TVCUSTOMQUALITY = settings.tvcustom_quality()
FURK_SORT = settings.furk_sort()
FURK_RESULTS = settings.furk_results()
IMDB_WATCHLIST = settings.imdb_watchlist_url()
IMDB_CUSTOMLIST_URL = settings.imdb_list_url()
UNAIRED = settings.show_unaired()
IMDB_LIST1 = settings.imdb_list1()
IMDB_LIST2 = settings.imdb_list2()
IMDB_LIST3 = settings.imdb_list3()
IMDB_LIST4 = settings.imdb_list4()
IMDB_LIST5 = settings.imdb_list5()
IMDB_LIST6 = settings.imdb_list6()
IMDB_LIST7 = settings.imdb_list7()
IMDB_LIST8 = settings.imdb_list8()
IMDB_LIST9 = settings.imdb_list9()
IMDB_LIST10 = settings.imdb_list10()
IMDB_LISTNAME1 = settings.imdb_listname1()
IMDB_LISTNAME2 = settings.imdb_listname2()
IMDB_LISTNAME3 = settings.imdb_listname3()
IMDB_LISTNAME4 = settings.imdb_listname4()
IMDB_LISTNAME5 = settings.imdb_listname5()
IMDB_LISTNAME6 = settings.imdb_listname6()
IMDB_LISTNAME7 = settings.imdb_listname7()
IMDB_LISTNAME8 = settings.imdb_listname8()
IMDB_LISTNAME9 = settings.imdb_listname9()
IMDB_LISTNAME10 = settings.imdb_listname10()
NZBMOVIE_URL = settings.nzvmovie_url()
FURK_LIM_FS = settings.furk_limit_file_size()
FURK_LIM_FS_NUM = settings.furk_limit_fs_num()
FURK_LIM_FS_MIN = settings.furk_limit_fs_min()
FURK_LIM_FS_TV = settings.furk_limit_file_size_tv()
FURK_LIM_FS_NUM_TV = settings.furk_limit_fs_num_tv()
FURK_PLAYLISTS = settings.furk_playlists()
FURK_FORMAT = settings.furk_format()
FURK_LIMIT = settings.furk_limit_result()
META_QUALITY = settings.meta_quality()
FURK_SEARCH_MF = settings.furk_search_myfiles()
ONECLICK_SEARCH = settings.oneclick_search()
QUALITYSTYLE = settings.qualitystyle()
QUALITYSTYLE_TV = settings.qualitystyle_tv()
PREFERRED2 = settings.preferred2()
CUSTOMQUALITY2 = settings.custom_quality2()
TVPREFERRED2 = settings.preferred_tv2()
TVCUSTOMQUALITY2 = settings.tvcustom_quality2()
DOWNLOAD_MOV = settings.movies_download_directory()
DOWNLOAD_TV = settings.tv_download_directory()
DOWNLOAD_MUS = settings.music_download_directory()
DOWNLOAD_SUB = settings.download_subtitles()
DOWNLOAD_TEMP = settings.temp_download_directory()
ACTIVE_DOWNLOADS = settings.downloads_file()
ACTIVE_DOWNLOADS_TV = settings.downloads_file_tv()
LIBRARY_FORMAT = settings.lib_format()
WISHLIST = settings.wishlist()
WISHLIST_FINISHED = settings.wishlist_finished()
PEOPLE_LIST = settings.people_list()
TRAILER_RESTRICT = settings.restrict_trailer()
TRAILER_QUALITY = settings.trailer_quality()
TRAILER_ONECLICK = settings.trailer_one_click()
F_DELAY = settings.furkdelay()
DOWNLOAD_MUS_VID = settings.music_video_download_directory()
SKIP_BROWSE = settings.skip_file_browse()
IMDB_RATING = settings.show_rating()
PC_ENABLE = settings.enable_pc()
PC_WATERSHED = settings.watershed_pc()
PC_RATING = settings.pw_required_at()
PC_PASS = settings.pc_pass()
PC_DEFAULT = settings.pc_default()
PC_TOGGLE = settings.enable_pc_settings()
DOWNLOAD_SPEED = settings.download_speed()
TEMP_PATH = settings.temp_path()
DPD = settings.download_play_delete()
THEME = settings.theme()

if THEME == "Blazetamer":
    fanart = os.path.join(ADDON.getAddonInfo('path'), 'art', THEME,'fanart.jpg')
else:
    fanart = os.path.join(ADDON.getAddonInfo('path'), 'art', THEME,'fanart1.jpg')

######################## DEV MESSAGE ###########################################################################################aw23
def dev_message():
    if ADDON.getSetting('dev_message')!="skip1.5.4":
        msg = os.path.join(ADDON.getAddonInfo('path'),'resources', 'messages', 'changelog.txt')
        TextBoxes("[B][COLOR red]Changelog[/B][/COLOR]",msg)
        ADDON.setSetting('dev_message', value='skip1.5.4') 

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()		
######################## DEV MESSAGE ###########################################################################################
def help_menu():
    addDir3('Changelog',"","help list menu","")
    addDir3('Parental Control',"","help list menu","")
    addDir3('Test Download Speed',"","test download","")


def help(text):
    header = "[B][COLOR red]" + text + "[/B][/COLOR]"
    text1 = text.replace(' ', '_').lower() + '.txt'
    msg = os.path.join(ADDON.getAddonInfo('path'),'resources', 'messages', text1)
    TextBoxes(header,msg)
    
    
######################## LOGIN ###########################################################################################
def login_at_furk():
    if FURK_ACCOUNT:
        if FURK.login(FURK_USER, FURK_PASS):
            return True
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Login failed", "The addon failed to login at Furk.net.", "Make sure you have confirmed your email and your", "login information is entered correctly in addon-settings")
            return False
    else:
        return False

def account_info():
    if not login_at_furk():
        return []
    try:	
        accinfo = FURK.account_info()
        text = []
        info = str(accinfo).replace("'","QTE")
	
        acctype = regex_from_to(info, 'nameQTE: uQTE', 'QTE, ')
     
        limit_mth = float(regex_from_to(info, 'bw_limit_monthQTE: uQTE', 'QTE, '))/1073741824
        used_bw_mth = float(regex_from_to(info, 'bw_used_monthQTE: uQTE', 'QTE, '))/1073741824
        rem_bw_mth = limit_mth - used_bw_mth
        multi_mth = regex_from_to(info, 'is_not_last_monthQTE: uQTE', 'QTE, ')
        if multi_mth == '1':
            text = "resets"
        else:
            text = "expires"
	
        bw_days_left = float(regex_from_to(info, 'bw_month_time_leftQTE: uQTE', 'QTE, '))/60/60/24
        rem_days = "%.1f" % bw_days_left
		


        dialog = xbmcgui.Dialog()
        dialog.ok(("Account Type: " + acctype) + " - " + ("%.0fGB" % limit_mth) + " pm", ("Current Month: " + '[COLOR red]' + ("%.1fGB" % used_bw_mth) + '[/COLOR]' + " / " + '[COLOR green]' + ("%.1fGB" % rem_bw_mth) + '[/COLOR]' + " / " + ("%.1fGB" % limit_mth)), "", ("Bandwidth limit " + text + " in " + str(rem_days) + " days"))

    except:
        accinfo = FURK.account_info()
        info = regex_from_to(str(accinfo).replace("'","QTE"), 'QTEbw_statsQTE', ']}') 
		
        
        all_bytes = regex_get_all(info, 'uQTEbytesQTE: u', ', uQTE')

        day1 = regex_from_to(all_bytes[0], 'QTE: uQTE', 'QTE, u')
        day2 = regex_from_to(all_bytes[1], 'QTE: uQTE', 'QTE, u')
        day3 = regex_from_to(all_bytes[2], 'QTE: uQTE', 'QTE, u')
        day4 = regex_from_to(all_bytes[3], 'QTE: uQTE', 'QTE, u')
        day5 = regex_from_to(all_bytes[4], 'QTE: uQTE', 'QTE, u') 
        day6 = regex_from_to(all_bytes[5], 'QTE: uQTE', 'QTE, u')
        day7 = regex_from_to(all_bytes[6], 'QTE: uQTE', 'QTE, u')
		
        if float(day1) > 1073741824:
            day1_tot =  float(day1)/1073741824
            day1_text = "%.2fGB" % day1_tot
        else:
            day1_tot = float(day1)/1048576
            day1_text = "%.1fMB" % day1_tot
			
        week_tot = int(day1) + int(day2) + int(day3) + int(day4) + int(day5) + int(day6) + int(day7)
        if float(week_tot) > 1073741824:
            week_total =  float(week_tot)/1073741824
            week_text = "%.2fGB" % week_total
        else:
            week_total =  float(week_tot)/1048576
            week_text = "%.1fMB" % week_total
        
        dialog = xbmcgui.Dialog()		
        dialog.ok("Account Type: Free", "Used Today: " + str(day1_text), "Last 7 Days: " + str(week_text))

######################## END LOGIN ###########################################################################################

######################## DOWNLOAD ###########################################################################################		
def download_play(name, url, type):
    ts = type.split('$')
    type = ts[0]
    MBs = ts[1]
    imdb_id = ts[2]
    MBs = round(float(MBs),0)
    if os.path.exists(TEMP_PATH):
        os.remove(TEMP_PATH)
    WAITING_TIME = (MBs * 7) + 8
    if type == "tv":
        directory=DOWNLOAD_TV
    elif type == "musicvid":
        directory=DOWNLOAD_MUS_VID
    elif type == "down_delete":
        directory = DOWNLOAD_TEMP
    else:
        directory=DOWNLOAD_MOV
    if type == "tv":
        data_path = os.path.join(directory, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThreadTV(name, url, data_path, WAITING_TIME)
        download_list = ACTIVE_DOWNLOADS_TV
    elif type == "musicvid":
        data_path = os.path.join(directory, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThread(name, url, data_path, WAITING_TIME)
        download_list = ACTIVE_DOWNLOADS
    else:
        data_path = os.path.join(directory, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThread(name, url, data_path, WAITING_TIME)
        download_list = ACTIVE_DOWNLOADS
    if directory == "set" or directory == "":
        xbmcgui.Dialog().ok('Download directory not set', 'Set your download path in settings first')
        ADDON.openSettings()
    else:
        dlThread.start()
        wait(2, "Download, Play, Delete.....starting")
        dp = xbmcgui.DialogProgress()
        dp.create('Wait for first 7 seconds to download')
        while (float(os.path.getsize(data_path))/1024/1024) < WAITING_TIME and xbmc.Player().isPlayingVideo() == False and os.path.exists(data_path):
            percent = min(((os.path.getsize(data_path)/1024/1024)  * 100/ int(WAITING_TIME)), 100)
            mbs = '%.0fMB of %.0fMB downloaded' % (os.path.getsize(data_path)/1024/1024, int(WAITING_TIME)) 
            dp.update(percent, mbs)
        if os.path.exists(data_path):
            if mode == "download play":
                scan_library()
                notify = "%s,%s,%s" % ('XBMC.Notification(Added to Library',name,'4000)')
                xbmc.executebuiltin(notify)
                size = get_file_size(url)
                list_data = "%s<|>%s<|>%s" % (name, data_path, size)
                add_search_query(list_data, download_list)
            ADDON.setSetting('temp_path', value=data_path)
            execute_video(name, data_path, imdb_id, strm=False)
        else:
            xbmcgui.Dialog().ok('Download failed', name)
	
def download_only(name, url, type):
    if os.path.exists(TEMP_PATH):
        os.remove(TEMP_PATH)
    
    WAITING_TIME = 5
    if type == "tv":
        directory=DOWNLOAD_TV
    elif type == "musicvid":
        directory=DOWNLOAD_MUS_VID
    else:
        directory=DOWNLOAD_MOV
    if type == "tv":
        data_path = os.path.join(directory, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThreadTV(name, url, data_path, WAITING_TIME)
        download_list = ACTIVE_DOWNLOADS_TV
    elif type == "musicvid":
        data_path = os.path.join(directory, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThread(name, url, data_path, WAITING_TIME)
        download_list = ACTIVE_DOWNLOADS
    else:
        data_path = os.path.join(directory, clean_file_name(name, use_blanks=False))
        dlThread = DownloadFileThread(name, url, data_path, WAITING_TIME)
        download_list = ACTIVE_DOWNLOADS
    print data_path[3:]
    if directory == "set" or directory == "":
        xbmcgui.Dialog().ok('Download directory not set', 'Set your download path in settings first')
        ADDON.openSettings()
    else:
        dlThread.start()
        if not name.endswith("srt"):
            if mode != "wishlist search":
                wait_dl_only(WAITING_TIME, "Starting Download")
                if os.path.exists(data_path):
                    notify = "%s,%s,%s" % ('XBMC.Notification(Download started',name,'4000)')
                    xbmc.executebuiltin(notify)
                    scan_library()
                    notify = 'XBMC.Notification(Added to Library,You can play from library now,4000)'
                    xbmc.executebuiltin(notify)
                    size = get_file_size(url)
                    list_data = "%s<|>%s<|>%s" % (name, data_path, size)
                    add_search_query(list_data, download_list)

                else:
                    xbmcgui.Dialog().ok('Download failed', name)
            else:
                time.sleep(6)
                if os.path.exists(data_path):
                    size = get_file_size(url)
                    list_data = "%s<|>%s<|>%s" % (name, data_path, size)
                    add_search_query(list_data, download_list)
				
def download_music(xbmcname, url, filename):
    if os.path.exists(TEMP_PATH):
        os.remove(TEMP_PATH)
    if xbmcname.find(' | ')>0:
        namesplit=xbmcname.split(' | ')
        artist=namesplit[0]
        album=namesplit[1]
    else:
        artist="My Files Downloads"
        album=xbmcname
    if mode=="download song" or (name[len(name)-4:] == ".zip" or name[len(name)-4:] == ".rar"):
        filename=filename
        url = "%s%s" % (url, name[len(name)-4:])
    else:
        filename = "%s%s" % (filename, ".zip")
        url = "%s%s" % (url, ".zip")
    artist_path = create_directory(DOWNLOAD_MUS, clean_file_name(artist, use_blanks=False))
    album_path = create_directory(artist_path, clean_file_name(album, use_blanks=False))
    if mode=="download song":
        data_path = os.path.join(album_path, filename)
    else:
        data_path = os.path.join(DOWNLOAD_MUS, filename)
    dlThread = DownloadMusicThread(filename, url, data_path, album_path)
    dlThread.start()
    notify = "%s,%s,%s" % ('XBMC.Notification(Download started',xbmcname,'4000)')
    xbmc.executebuiltin(notify)

def download_kat(queryname, episode):
    menu_texts = []
    menu_data = []
    menu_url = []
    menu_page_url = []
    dialog = xbmcgui.Dialog()
    episode1 = episode.replace("dummy", "")
    list_name = queryname
    queryname = queryname.replace(" any", "")

    data_url = "http://kickass.to/hourlydump.txt.gz"
    data_path = os.path.join(DOWNLOAD_PATH, "kat.gz")
    if not os.path.exists(data_path):
        print "[What the Furk...XBMCHUB.COM].........daily torrent file does not exist, downloading"
        try:
            urllib.urlretrieve(data_url, data_path)
        except:
            xbmc.log("[What the Furk...XBMCHUB.COM] KAT URL request timed out")
            display_error("kickasstorrents URL request timed out", "Is the website down or blocked?")
    else:
        currenttime = time.time()
        filetime = os.path.getmtime(data_path)
        diff = currenttime - filetime
        if diff > 3600:
            print "[What the Furk...XBMCHUB.COM].........over 1 hour since last torrent file, downloading"
            try:
                urllib.urlretrieve(data_url, data_path)
            except:
                xbmc.log("[What the Furk...XBMCHUB.COM] KAT URL request timed out")
                display_error("kickasstorrents URL request timed out", "Is the website down or blocked?")
        else:
            print "[What the Furk...XBMCHUB.COM].........less than 1 hour since last torrent file, use current file"
    kat_list = gzip.open(data_path)
    kat_list = kat_list.read()
    search_list = kat_list.split('\n')
    for list in search_list:
        if list != '':
            list = list.split('|')
            info_hash = list[0]
            name = list[1]
            type = list[2]
            page_url = list[3]
            url_dl = list[4]
            if queryname.find(" ")>0:
                filename = queryname.lower().split(" ")
                if  filename[0] in name.lower() and filename[1] in name.lower() and episode1.lower() in name.lower() and (type == "Movies" or type == "TV"):#  and queryname[1] in name.lower() and queryepisode in name.lower()
                    menu_texts.append(name)
                    menu_data.append(info_hash)
                    menu_url.append(url_dl)
                    menu_page_url.append(page_url)
            else:
                filename = queryname.lower()
                if  filename in name.lower() and episode1.lower() in name.lower() and (type == "Movies" or type == "TV"):
                    menu_texts.append(name)
                    menu_data.append(info_hash)
                    menu_url.append(url_dl)
                    menu_page_url.append(page_url)
			
    if len(menu_data) == 0:
        if mode != "wishlist search":
            dialog = xbmcgui.Dialog()
            dialog.ok("No torrents found", "The search was unable to find any torrents", "%s %s" % (queryname, episode1))
            return (None, None)
    else:
        if mode == "wishlist search":
            if len(menu_data) == 0:
                return (None, None)
            else:
                menu_id = 0
                info_hash = str(menu_data[menu_id])
                name = str(menu_texts[menu_id])
                add_download(name, info_hash)
                action = "newtorrents"
                list_data = "%s<|>%s<|>%s" % (list_name, action, episode)
                remove_search_query(list_data, WISHLIST)
                add_search_query(list_data, WISHLIST_FINISHED)
        else:
            menu_id = dialog.select('Select Torrent', menu_texts)
            if(menu_id < 0):
                return (None, None)
                dialog.close()
            else:	
                info_hash = str(menu_data[menu_id])
                name = str(menu_texts[menu_id])
                add_download(name, info_hash)

def test_dl_speed():
    dialog = xbmcgui.Dialog()
    dp = xbmcgui.DialogProgress()
    dp.create('Downloading a test file from Furk.net')
    url_19 = 'http://ic229fiisepcj1f8tktpf424lsf34h18q0kedd8.gcdn.biz/d/p/fMmKl_3o3UBC3GmMrkJMFpA-yc4EQwxcHjJEKNAo5rU/Michael%20Connelly'
    url_39 = "http://suq2ids38j823htmikc64nuc38f34h18q0kedd8.gcdn.biz/d/p/BKdtx4zKAgt6Ynzi56S5cSEUE_xGruZDxuJ9l8opOhvvs8cCdCK0vx4yRCjQKOa1/Extras%2FSeason%2003%2FStargate%20SG-1%20Season%2003%20Extra%2001%20-%20Season%203%20-%20Trailer.avi"
    url_54 = 'http://am38oja80gso3qj1fkev827b4kf34h18q0kedd8.gcdn.biz/d/p/nuBP-fhgYNY3tV7Lh07Hx3SAnKSAkEEtHjJEKNAo5rU/%5Bebook%20Brasil%5D%20Kindle%20-%2028082011%20-%20100%20livros%20-%20vol%20002.zip'
    path = os.path.join(META_PATH, "test_download.avi")
    start_time = time.time()
    try:
        urllib.urlretrieve(url_39, path, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))
    except:
        if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError):
            end_time = time.time()
            size = float(os.path.getsize(path)) * 8
            kbps_speed = size / (end_time - start_time)
            kbps_speed = kbps_speed / 1024 / 1024
            e = 'File downloaded at %.02f Mb/s ' % kbps_speed		
            xbmcgui.Dialog().ok('Download cancelled!',e)
            ADDON.setSetting('download_speed', value=str(kbps_speed))
            return False 
        else: 
            raise
        return False
    end_time = time.time()
    size = float(os.path.getsize(path)) * 8
    kbps_speed = size / (end_time - start_time)
    kbps_speed = kbps_speed / 1024 / 1024
    e = 'File downloaded at %.02f Mb/s ' % kbps_speed
    dialog.ok("Speed Test Result", e)
    ADDON.setSetting('download_speed', value=str(kbps_speed))
	
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
    try: 
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 / 1024 * 8
        total = float(filesize) / (1024 * 1024) 
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
        e = 'Speed: %.02f Mb/s ' % kbps_speed 
        e += 'ETA: %02d:%02d' % divmod(eta, 60) 
        dp.update(percent, mbs, e)
    except: 
        percent = 100 
        dp.update(percent) 
    if dp.iscanceled(): 
        dp.close()
        raise StopDownloading('Stopped Downloading')
		
class StopDownloading(Exception): 
    def __init__(self, value): 
        self.value = value 
    def __str__(self): 
        return repr(self.value)

def download_meta_zip():
    menu_data = ["",
                  "http://wtf.gosub.dk/low.zip",
                  "http://wtf.gosub.dk/medium.zip",
                  "http://wtf.gosub.dk/high.zip",
                  "http://wtf.gosub.dk/medium.zip"]
    menu_texts = ["Don't download",
                 "Download low quality images [123MB]",
                 "Download mid quality images [210MB]",
                 "Download high quality images [508MB]",
                 "Download maximum quality images [722MB]"]
    data_url = "http://wtf.gosub.dk/data-338438.zip"
    
    dialog = xbmcgui.Dialog() 
    menu_id = dialog.select('Select file', menu_texts)
    if menu_id < 1:
        return
    
    ADDON.setSetting('meta_quality', value=str(menu_id + 1))
    
    try:
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Searching for files')
        
        meta_url = menu_data[menu_id]
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading meta...")
        meta_path = os.path.join(DOWNLOAD_PATH, "meta.zip")
        download(meta_url, meta_path, pDialog)
        xbmc.log("[What the Furk...XBMCHUB.COM] Extracting meta...")
        xbmc.executebuiltin("XBMC.Extract(%s , %s)" % (meta_path, META_PATH))
        xbmc.log("[What the Furk...XBMCHUB.COM] ...done!")
        data_path = os.path.join(DOWNLOAD_PATH, "data.zip")
        download(data_url, data_path, pDialog)
        xbmc.executebuiltin("XBMC.Extract(%s , %s)" % (data_path, META_PATH))
        xbmc.log("[What the Furk...XBMCHUB.COM] All done!")
    except:
        dialog.ok("Setup meta data", "Unable to reach the host server.")
######################## END DOWNLOAD ###########################################################################################
def get_subscriptions():
    try:
        content = read_from_file(SUBSCRIPTION_FILE)
        lines = content.split('\n')
        
        for line in lines:
            data = line.split('\t')
            if len(data) == 2:
                if data[1].startswith('tt'):
                    tv_show_name = clean_file_name(data[0].split('(')[0][:-1])
                    tv_show_imdb = data[1]
                    tv_show_mode = "strm tv show dialog"
                    create_tv_show_strm_files(tv_show_name, tv_show_imdb, tv_show_mode, TV_SHOWS_PATH)
                else:
                    mode = data[1]
                    items = get_menu_items(name, mode, "1", "")
                    
                    for (url, li, isFolder) in items:
                        paramstring = url.replace(sys.argv[0], '')
                        params = get_params(paramstring)
                        movie_name = urllib.unquote_plus(params["name"])
                        movie_data = urllib.unquote_plus(params["name"])
                        movie_imdb = urllib.unquote_plus(params["imdb_id"])
                        movie_mode = "strm movie dialog"
                        print movie_name
                        if 'Next Page' not in movie_name:
                            create_strm_file(movie_name, movie_data, movie_imdb, movie_mode, MOVIES_PATH)
        time.sleep(2)
        xbmc.executebuiltin('UpdateLibrary(video)')
                    
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Failed to fetch subscription")

def subscription_index(name, mode):
    try:
        content = read_from_file(SUBSCRIPTION_FILE)
        line = str(name) + '\t' + str(mode)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1 #Not subscribed

def subscribe(name, mode):
    if subscription_index(name, mode) >= 0:
        return
    content = str(name) + '\t' + str(mode) + '\n'
    write_to_file(SUBSCRIPTION_FILE, content, append=True)
    
def unsubscribe(name, mode):
    index = subscription_index(name, mode)
    if index >= 0:
        content = read_from_file(SUBSCRIPTION_FILE)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        
        if len(s) == 0:
            os.remove(SUBSCRIPTION_FILE)
        else:
            write_to_file(SUBSCRIPTION_FILE, s)
    
def find_search_query(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1 #Not found

def daily_torrents():
    search_file = os.path.join(DOWNLOAD_PATH, "hourlydump.txt")
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        return lines
    except:
        return -1
    
def add_search_query(query, search_file):
    if find_search_query(query, search_file) >= 0:
        return

    if os.path.isfile(search_file):
        content = read_from_file(search_file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % query
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(search_file, s)
    
def remove_search_query(query, search_file):
    index = find_search_query(query, search_file)
    if index >= 0:
        content = read_from_file(search_file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(search_file, s)
    
def create_strm_file(name, data, imdb_id, mode, dir_path):
    try:
        strm_string = create_url(name, mode, data=data, imdb_id=imdb_id)
        filename = clean_file_name("%s.strm" % name)
        path = os.path.join(dir_path, filename)
        stream_file = open(path, 'w')
        stream_file.write(strm_string)
        stream_file.close()
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Error while creating strm file for : " + name)

def toggle_one_click():
    if ONECLICK_SEARCH:
        ADDON.setSetting('oneclick_search', value='false')
        notification("WTF - One-Click Search", "TURNED OFF")
    else:
        ADDON.setSetting('oneclick_search', value='true')
        notification("WTF - One-Click Search", "TURNED ON")
    if mode != "mainenance menu":
        xbmc.executebuiltin('xbmc.activatewindow(0)')
	
def create_tv_show_strm_files(name, imdb_id, mode, dir_path):
    info = TheTVDBInfo(imdb_id)
    episodes = info.episodes()
    
    tv_show_path = create_directory(dir_path, name)
    for episode in episodes:
        first_aired = episode.FirstAired()
        if len(first_aired) > 0:
            d = first_aired.split('-')
            episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            if date.today() > episode_date:
                season_number = int(episode.SeasonNumber())
                if season_number > 0:
                    episode_number = int(episode.EpisodeNumber())
                    episode_name = episode.EpisodeName()
                    display = "[S%.2dE%.2d] %s" % (season_number, episode_number, episode_name)
                    data = '%s<|>%s<|>%d<|>%d' % (name, episode_name, season_number, episode_number)
                    season_path = create_directory(tv_show_path, str(season_number))
                    create_strm_file(display, data, imdb_id, mode, season_path)
					

def remove_strm_file(name, dir_path):
    try:
        filename = "%s.strm" % (clean_file_name(name, use_blanks=False))
        path = os.path.join(dir_path, filename)
        os.remove(path)
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Was unable to remove movie: %s" % (name)) 

def remove_tv_show_strm_files(name, dir_path):
    try:
        path = os.path.join(dir_path, name)
        shutil.rmtree(path) 
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] Was unable to remove TV show: %s" % (name)) 
    
############################### MAINTENANCE #############################################################################
def deletecachefiles():
	# Set path to What th Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
		
    for root, dirs, files in os.walk(wtf_cache_path):
        file_count = 0
        file_count += len(files)
	
    # Count files and give option to delete
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete WTF Cache Files", "There are no cache files to delete")
	
    # Check if platform is ATV2.....if yes count files and give option to delete	
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
		file_count = 0
        file_count += len(files)
		
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete Cache Files", "There are no ATV2 'Other' cache files to delete")
			
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
		file_count = 0
        file_count += len(files)
		
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete Cache Files", "There are no ATV2 'LocalAndRental' cache files", "to delete")

def deletemetazip():
	# Set path to What the Furk meta downloads
    wtf_metazip_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/download'), '')
		
    for root, dirs, files in os.walk(wtf_metazip_path):
        file_count = 0
        file_count += len(files)
	
    # Count files and give option to delete
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete WTF Zip Downloads", str(file_count) + " files found", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete WTF Zip Downloads", "There are no files to delete")
			
def move_meta():
    root_src_dir = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/meta'), '')
    root_dst_dir = META_PATH

    dialog = xbmcgui.Dialog()
    if dialog.yesno("Do you want to copy files to:", META_PATH, "This may take a while!"):
        try:
            for src_dir, dirs, files in os.walk(root_src_dir):
                file_count = 0
                file_count += len(files)
                dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
                if not os.path.exists(dst_dir):
                    os.mkdir(dst_dir)
                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    shutil.move(src_file, dst_dir)
            dialog = xbmcgui.Dialog()
            dialog.ok("DONE!", root_src_dir, "is now empty")
 
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("Move meta files", "Unable to move your files", "You may need to try manually")
			
def deletepackages():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Delete Packages", "Success")
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok("Delete Packages", "Unable to delete")
			
def deletesearchlists():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete IMDB search list", "Do you want to clear the list?"):
        fo=open(IMDB_SEARCH_FILE,"wb")
		
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Furk search list", "Do you want to clear the list?"):
        fo=open(FURK_SEARCH_FILE,"wb")
		
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Furk search list", "Do you want to clear the list?"):
        fo=open(IMDB_ACTOR_FILE,"wb")
		
def deletewishlists():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Pending Wishlist", "Do you want to clear the list?"):
        fo=open(WISHLIST,"wb")
		
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Finished Wishlist", "Do you want to clear the list?"):
        fo=open(WISHLIST_FINISHED,"wb")
		
def deletemetafiles():
	# Set path to What the Furk meta files
    wtf_meta_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/meta'), '')
    for root, dirs, files in os.walk(wtf_meta_path):
        file_count = 0
        file_count += len(files)
	
    # Count files and give option to delete
        if file_count > 0:

            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Meta Files from userdata directory", str(file_count) + " files found", "Do you want to delete them?"):
			
                for f in files:
    	            os.unlink(os.path.join(root, f))
                for d in dirs:
    	            shutil.rmtree(os.path.join(root, d))
					
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("Delete WTF Meta Files", "There are no files to delete")
		
############################### END MAINTENANCE #############################################################################

def search_nzbmovie(params):
    movies = []
    count = 0
    while count < IMDB_RESULTS:
        try:
            body = nzbmovie_search(params, str(count))
            try:
                movies.extend(get_nzbmovie_search_result(body))
            except:
                xbmc.log("[What the Furk...XBMCHUB.COM] NZB Movie Seeker regex error")
                display_error("Unable to scrape nzbmovieseeker.com", "Page structure may have changed")
        except:
            xbmc.log("[What the Furk...XBMCHUB.COM] NZB Movie Seeker URL request timed out")
            display_error("NZB Movie Seeker URL request timed out", "Is the website down?")
        count = count + 250
        count = count + 250
        if len(movies) < count:
            return movies
        setView('movies', 'movies-view')    
    return movies
    setView('movies', 'movies-view')
	
def nzbmovie_search(params, start="1"):
    print params
    url = NZBMOVIE_URL + params
    print url
    try:
        body = get_url(url, cache=CACHE_PATH)
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] NZB Movie Seeker URL request timed out")
    return body
    
def get_nzbmovie_search_result(body):
    all_tr = regex_get_all(body, '<div class="release-wrapper">', '<div class="rating')
    
    movies = []
    for tr in all_tr:
        all_td = regex_get_all(tr, '<h3>', '</h3>')
        imdb_id = 'tt' + regex_from_to(all_td[0], 'NZB/', '-')
        name = regex_from_to(all_td[0], 'title">', '<').replace(':',' ')

        movies.append({'imdb_id': imdb_id, 'name': name, 'year': 'rem'})
    return movies
	

def search_imdb(url,start,pname):
    movies = []
    try:
        body = get_url(url, cache=CACHE_PATH)
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out")
    	
    all_tr = regex_get_all(body, '<tr class=', '</tr>')
    for tr in all_tr:
       
        all_td = regex_get_all(tr, '<td', '</td>')
        imdb_id = regex_from_to(all_td[1], '/title/', '/')
        name = regex_from_to(all_td[1], '/">', '</a>')
        year = regex_from_to(all_td[1], '<span class="year_type">\(', '\)')
        try:
            rating = regex_from_to(all_td[2], '<b>', '</b>')
            votes = regex_from_to(all_td[3], '\n', '\n')
        except:
            rating = ""
            votes = ""

        movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes})
    p_start = int(start) + IMDB_RESULTS
    p_end = (int(start) + (IMDB_RESULTS * 2)) -1
    if pname != "search":
        movies.append({'imdb_id': str(pname), 'name': '[COLOR gold]' + "%s (%s-%s)" % (">>> Next Page",str(p_start),str(p_end)) + '[/COLOR]', 'year': "rem", 'rating': start, 'votes': "NP"})

    return movies
    
    setView('movies', 'movies-view')

	
def watchlist_imdb(url,start,pname):
    movies = []
    try:
        body = get_url(url, cache=CACHE_PATH)
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out")
    all_tr = regex_get_all(body, '<tr data-item', '</tr>')
     
    for tr in all_tr:
        all_td = regex_get_all(tr, '<td', 'td>')
        imdb_id = regex_from_to(all_td[1], 'title/', '/')
        name = regex_from_to(all_td[1], '/">', '</a>')
        year = regex_from_to(all_td[2], 'year">', '</td>')
        try:
            rating = regex_from_to(all_td[6], 'user_rating">', '</')
            votes = regex_from_to(all_td[7], 'num_votes">', '</')
        except:
            rating = ""
            votes = ""
        movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes})
    p_start = int(start) + 250
    p_end = (int(start) + (250 * 2)) -1
    movies.append({'imdb_id': str(pname), 'name': '[COLOR gold]' + "%s (%s-%s)" % (">>> Next Page",str(p_start),str(p_end)) + '[/COLOR]', 'year': "rem", 'rating': start, 'votes': "NW"})
    return movies
    setView('movies', 'movies-view')
	
def customlist_imdb(list):
    movies = []
    url = IMDB_CUSTOMLIST_URL + list + "/?start=1&view=compact&sort=listorian:asc"
    try:
        body = get_url(url, cache=CACHE_PATH)
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out")
    all_tr = regex_get_all(body, '<td class="listorian', '</tr>')

    for tr in all_tr:
        all_td = regex_get_all(tr, '<td', 'td>')
        imdb_id = regex_from_to(all_td[1], 'title/', '/')
        name = regex_from_to(all_td[1], '/">', '</a><')
        year = regex_from_to(all_td[2], 'year">', '</')
        try:
            rating = regex_from_to(all_td[6], 'user_rating">', '</')
            votes = regex_from_to(all_td[7], 'votes">', '</')
        except:
            rating = ""
            votes = ""
        movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes}),
    return movies
    setView('movies', 'movies-view')
	
def search_actors(params):
    actors = []
    body = []
    url = "%s%s" % (IMDB_ACTOR_SEARCH, urllib.urlencode(params))
    try:
        body = get_url(url, cache=CACHE_PATH)
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out") 
		
    all_tr = regex_get_all(body, '<tr class=', '</tr>')
    for tr in all_tr:
        all_td = regex_get_all(tr, '<td', '</td>')
        imdb_id = regex_from_to(all_td[2], 'href="/name/', '/')
        name = regex_from_to(all_td[2], '/">', '</a>')
        try:
            profession = regex_from_to(all_td[2], 'description">', ', <a href')
        except:
            profession = ""
        photo = regex_from_to(all_td[1], '<img src="', '" ')
        photo = photo.replace("54", "214").replace("74", "314").replace("CR1", "CR12")
        actors.append({'name': name, 'imdb_id': imdb_id, 'photo': photo, 'profession': profession})
    return actors

def get_items_in_dir(path):
    items = []
    for dirpath, dirnames, filenames in os.walk(path): 
        for subdirname in dirnames: 
            items.append(subdirname) 
        for filename in filenames:
            if filename.endswith(".strm"): 
                items.append(filename[:-5])
        
    return items

def exist_in_dir(name, path, isMovie=False):
    if isMovie:
        name = "%s.strm" % name
    item_list = os.listdir(path)
    
    for item in item_list:
        if item == name:
            return True
    return False

#Menu
	
def main_menu():
    items = []
    items.append(create_directory_tuple('Movies', 'imdb menu'))
    items.append(create_directory_tuple('TV Shows', 'imdb tv menu'))
    items.append(create_directory_tuple('Music', 'music menu'))
    items.append(create_directory_tuple('Search', 'search menu'))
    items.append(create_directory_tuple('My Files', 'my files directory menu'))
    items.append(create_directory_tuple('My People', 'people list menu'))
    items.append(create_directory_tuple('Watchlists', 'imdb list menu'))
    items.append(create_directory_tuple('Subscriptions', 'subscription menu'))
    items.append(create_directory_tuple('Account Info', 'account info'))
    items.append(create_directory_tuple('Maintenance', 'maintenance menu'))
    items.append(create_directory_tuple('Help', 'help menu'))
    return items

def imdb_similar_menu(name, data, imdb_id):
    movies=[]
    url = "%s%s%s" % ('http://m.imdb.com/title/',imdb_id,'/similarities')
    try:
        body = get_url(url, cache=CACHE_PATH)
        try:
            body = body.replace('\n',''	).replace('(','AX').replace(')','AZ')
            print body
            all_tr = regex_from_to(body, '<section class="similarities posters">', '</section>')
            match = re.compile('<a href="/title/(.+?)/">(.+?)</a> AX(.+?)AZ').findall(all_tr)
            movies.append({'imdb_id': imdb_id, 'name': '[COLOR cyan]' + 'IMDB USERS WHO LIKE ' + '[/COLOR]' + '[COLOR gold]' + clean_file_name(name, use_blanks=False).replace(' TV Series','').replace(' Mini-Series','').replace(' TV Special','') +  '[/COLOR]' + '[COLOR cyan]' + ' ALSO LIKE:' + '[/COLOR]', 'year': 'rem', 'rating': "", 'votes': "D"})
            for imdb_id,name,year in match:
                movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': "", 'votes': ""})
        except:
            xbmc.log("[What the Furk...XBMCHUB.COM] IMDB SIMILARITIES regex error")
            display_error("Unable to scrape imdb.com/similarities", "Page structure may have changed")
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] IMDB URL request timed out")
        display_error("IMDB (similarities) URL request timed out", "Is the website down?")
        movies.append({'imdb_id': "", 'name': "error", 'year': "visit www.xbmchub.com", 'rating': "", 'votes': ""})
    
    if data == "MOV":
        return create_movie_items(movies,"","")
    else:
        return create_tv_show_items(movies,"","")
	
def dvd_release_menu():
    now = time.strftime("%Y-%m")
    url = 'http://www.ondvdreleases.com/new-dvd-releases-%s/' % now
    body = get_url(url, cache=CACHE_PATH)
    match = re.compile('<li class="genre">(.+?)<a href="(.+?)"(.+?)>(.+?)</a></li>').findall(body)
    for num,url,d1,title in match:
        url = 'http://www.ondvdreleases.com' + url
        addDir(title,url,'dvd releases menu','')

def dvd_releases(url):
    items = []
    movies = []
    body = get_url(url, cache=CACHE_PATH)#thumb,w,h,title,year
    data = regex_from_to(body, '<div class="rline"></div>', '<br />')
    match = re.compile('<img src="(.+?)" width="(.+?)" height="(.+?)" alt="(.+?) (.+?)"').findall(data)
    for thumb,w,h,name,year in match:
        print name
        thumb = 'http://www.ondvdreleases.com' + thumb
        imdb_id = ""
        year = year
        rating = ""
        votes = ""
        addDir(clean_file_name(name),'url','movie result menu',thumb)
    return create_movie_items(movies,"","") 
    

def threed_menu():#
    items = []
    items.append(create_subdirectory_tuple('Title','3d result menu','http://www.blu-ray.com/movies/search.php?action=search&other_bluray3d=1&sortby=title&page=0<>'))
    items.append(create_subdirectory_tuple('Popularity','3d result menu','http://www.blu-ray.com/movies/search.php?action=search&other_bluray3d=1&sortby=popularity&page=0<>'))
    items.append(create_subdirectory_tuple('Release Date','3d result menu','http://www.blu-ray.com/movies/search.php?action=search&other_bluray3d=1&sortby=releasetimestamp&page=0<>'))
    return items

def threed_releases(url):
    url1 = url.replace('<>','')
    page = regex_from_to(url, 'page=', '<>')
    nextpage = int(page) + 1
    npurl = 'http' + regex_from_to(url, 'http', 'page=') + 'page=' + str(nextpage) + '<>'
    items = []
    movies = []
    body = get_url(url1, cache=CACHE_PATH).replace('\n', '').replace('\t', '')#url,d1,icon,title
    #print body
    #data = regex_from_to(body, 'Displaying results from', '<br><br><br><table width')
    match = re.compile('<a href="(.+?)">(.+?)img width="(.+?)" height="(.+?)" border="(.+?)" src="(.+?)" title="(.+?)"').findall(body)
    dupname = []
    for url,d1,d2,d3,d4,icon,title in match:
        imdb_id = ""
        name = title.replace(' (Blu-ray)', '').replace('  ', ' ')
        if not ' 3D' in name:
            if not '3D 'in name:
                name = name + ' 3D'
        year = "rem"
        rating = ""
        votes = ""
        infoLabels = get_meta(name.replace(' 3D', '').replace('3D ', ''),'movie',year="")
        if infoLabels['title']=='':
             name=name
        else:
            name=infoLabels['title'] + ' 3D'
        if infoLabels['cover_url']=='':
            iconimage=icon
        else:
            iconimage=infoLabels['cover_url']
        if not name.lower() in dupname:
            dupname.append(name.lower())
            addDir(clean_file_name(name),url,'movie result menu',iconimage,infoLabels=infoLabels)
    addDir('>>> Next page',npurl,'3d result menu','')
   
    return create_movie_items(movies,"","") 

def get_meta(name,types=None,year=None):
    if 'movie' in types:
        meta = metainfo.get_meta('movie',name,year)
    infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Aired': meta['premiered']}
        
    return infoLabels  	

def search_menu():
    items = []
    items.append(create_directory_tuple('Search Furk', 'furk search menu'))
    items.append(create_directory_tuple('Search People', 'imdb actor menu'))
    return items
	
def maintenance():
    items = []
    items.append(create_directory_tuple('Update Subscriptions (scheduled for ' + ADDON.getSetting('service_time') +')', 'force subscriptions'))
    items.append(create_directory_tuple('Update Library', 'scan library'))
    items.append(create_directory_tuple('Delete Cache Files', 'delete cache'))
    if ADDON.getSetting('meta_custom_directory') == "true":
        items.append(create_directory_tuple('Move Meta Files', 'move metafiles'))
    items.append(create_directory_tuple('Delete Meta Files', 'delete metafiles'))
    items.append(create_directory_tuple('Delete Meta Zip Files', 'delete meta zip'))
    items.append(create_directory_tuple('Delete Packages', 'delete packages'))
    items.append(create_directory_tuple('Clear Search Lists', 'delete search lists'))
    items.append(create_directory_tuple('Clear Wishlists', 'delete wishlists'))
    items.append(create_directory_tuple('Toggle One-Click', 'toggle one-click'))
    if PC_TOGGLE == 'LOCKED':
        items.append(create_directory_tuple('[COLOR green]' + 'UNLOCK Parental Control Settings' + '[/COLOR]', 'enable pc setting'))
    else:
        items.append(create_directory_tuple('[COLOR red]' + 'LOCK Parental Control Settings' + '[/COLOR]', 'enable pc setting'))
    return items
	
def myfiles_directory():
    items = []
    items.append(create_directory_tuple('My Files - Finished', 'my files menu'))
    items.append(create_directory_tuple('My Files - Deleted', 'my files deleted menu'))
    items.append(create_directory_tuple('Wishlist - Pending', 'wishlist pending menu'))
    items.append(create_directory_tuple('Wishlist - Finished', 'wishlist finished menu'))
    items.append(create_directory_tuple('[COLOR gold]' + ">> Run Wishlist Search <<" + '[/COLOR]', 'wishlist search'))
    items.append(create_directory_tuple('Downloaded - Movies', 'download movies menu'))
    items.append(create_directory_tuple('Downloaded - TV Episodes', 'download episodes menu'))
    items.append(create_directory_tuple('Active Downloads', 'active download menu'))
    items.append(create_directory_tuple('Failed Downloads', 'failed download menu'))
    return items
	

def imdb_menu():
    items = []
    items.append(create_movie_directory_tuple('Top Movies', 'all movies menu', '1')) 
    items.append(create_movie_directory_tuple('New Movies', 'new movies menu', '1'))
    items.append(create_movie_directory_tuple('Coming Soon', 'movies soon menu', '1'))
    items.append(create_directory_tuple('DVD Releases', 'dvd release menu'))
    items.append(create_directory_tuple('3D Movies', '3d menu'))
    items.append(create_directory_tuple('Movies by MPAA Rating', 'movie mpaas menu'))
    items.append(create_directory_tuple('Movies by Genre', 'movie genres menu')) 
    items.append(create_directory_tuple('Movies by Group', 'movie groups menu'))
    items.append(create_directory_tuple('Movies by Studio', 'movie studios menu'))
    items.append(create_directory_tuple('Scene Releases', 'nzbmovie menu'))	
    items.append(create_movie_directory_tuple('Blu-Ray at Amazon', 'blu-ray menu', '1'))
    items.append(create_directory_tuple('Search', 'imdb search menu'))
    return items
	
def imdb_menu_tv():
    items = []
    items.append(create_movie_directory_tuple('Top TV Shows', 'all tv shows menu','1'))  
    items.append(create_directory_tuple('TV shows by Genre', 'tv show genres menu'))
    items.append(create_directory_tuple('TV shows by Group', 'tv show groups menu'))	
    items.append(create_movie_directory_tuple('Active TV Shows', 'active tv shows menu','1'))
    items.append(create_directory_tuple('Search', 'imdb search tv menu'))
    return items

def music_menu():
    items = []
    items.append(create_subdirectory_tuple('Search Artist','search artist menu',''))
    items.append(create_subdirectory_tuple('Search Album','search album menu',''))
    items.append(create_subdirectory_tuple('Charts','chart menu',''))
    items.append(create_subdirectory_tuple('My Files (Furk)','my files audio menu',''))
    return items
	
def chart_menu():
    items = []
    items.append(create_subdirectory_tuple('UK Album Chart','billboard menu','http://www1.billboard.com/charts/united-kingdom-albums'))
    items.append(create_subdirectory_tuple('BillBoard 200','billboard menu','http://www1.billboard.com/charts/billboard-200'))
    items.append(create_subdirectory_tuple('Hot 100 Singles','billboard menu','http://www1.billboard.com/charts/hot-100'))
    items.append(create_subdirectory_tuple('Country Albums','billboard menu','http://www1.billboard.com/charts/country-albums'))
    items.append(create_subdirectory_tuple('HeatSeeker Albums','billboard menu','http://www1.billboard.com/charts/heatseekers-albums'))
    items.append(create_subdirectory_tuple('Independent Albums','billboard menu','http://www1.billboard.com/charts/independent-albums'))
    items.append(create_subdirectory_tuple('Catalogue Albums','billboard menu','http://www1.billboard.com/charts/catalog-albums'))
    items.append(create_subdirectory_tuple('Folk Albums','billboard menu','http://www1.billboard.com/charts/folk-albums'))
    items.append(create_subdirectory_tuple('Blues Albums','billboard menu','http://www1.billboard.com/charts/blues-albums'))
    items.append(create_subdirectory_tuple('Tastemaker Albums','billboard menu','http://www1.billboard.com/charts/tastemaker-albums'))
    items.append(create_subdirectory_tuple('Rock Albums','billboard menu','http://www1.billboard.com/charts/rock-albums'))
    items.append(create_subdirectory_tuple('Alternative Albums','billboard menu','http://www1.billboard.com/charts/alternative-albums'))
    items.append(create_subdirectory_tuple('Hard Rock Albums','billboard menu','http://www1.billboard.com/charts/hard-rock-albums'))
    items.append(create_subdirectory_tuple('Digital Albums','billboard menu','http://www1.billboard.com/charts/digital-albums'))
    items.append(create_subdirectory_tuple('R&B Albums','billboard menu','http://www1.billboard.com/charts/r-b-hip-hop-albums'))
    items.append(create_subdirectory_tuple('Top R&B/Hip-Hop Albums','billboard menu','http://www1.billboard.com/charts/r-and-b-albums'))
    items.append(create_subdirectory_tuple('Dance Electronic Albums','billboard menu','http://www1.billboard.com/charts/dance-electronic-albums'))
	
    return items

def nzbmovie_menu():
    items = []
    items.append(create_movie_directory_tuple('Top Downloads - This Week', 'nzbweek menu', ''))
    items.append(create_movie_directory_tuple('Top Downloads - This Month', 'nzbmonth menu', ''))
    items.append(create_movie_directory_tuple('Top Downloads - This Year', 'nzbyear menu', ''))
    items.append(create_movie_directory_tuple('Most Requested', 'nzbwatchlist menu', '')) 	
    return items
	
def imdb_list_menu():
    items = []
    items.append(create_movie_directory_tuple('My Watchlist - Movies', 'watchlist menu', '1'))
    items.append(create_movie_directory_tuple('My Watchlist - TV Shows', 'watchlist tv menu', '1'))
    items.append(create_movie_directory_tuple(IMDB_LISTNAME1, 'list1 menu','1'))
    items.append(create_movie_directory_tuple(IMDB_LISTNAME2, 'list2 menu', '1')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME3, 'list3 menu', '1')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME4, 'list4 menu', '1')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME5, 'list5 menu', '1')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME6, 'list6 menu', '1')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME7, 'list7 menu', '1')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME8, 'list8 menu', '1')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME9, 'list9 menu', '1')) 
    items.append(create_movie_directory_tuple(IMDB_LISTNAME10, 'list10 menu', '1')) 	
    return items

def movies_all_menu(start, name):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_TOP_MOV
    params["title_type"] = "feature,documentary,tv_movie"
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["production_status"] = PRODUCTION_STATUS
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    movies = search_imdb(url,start,name)
    return create_movie_items(movies, nstart, name)
	
def movies_actors_menu(name, imdb_id):
    items = []
    files = []
    movies = []
    start = "1"
        
    dialog = xbmcgui.Dialog()
    filmtype_list = ["Actor","Actress", "Director", "Writer", "Producer", "Miscellaneous Crew", "Cinematographer", "Soundtrack", "Editor", "Self"]
    filmtype_list_return = ["actor", "actress", "director", "writer", "producer", "miscellaneous crew", "cinematographer", "soundtrack", "editor", "self"]
    
    filmtype_id = dialog.select(name, filmtype_list)
    if(filmtype_id < 0):
        return (None, None)
        dialog.close()
    
    type = filmtype_list_return[filmtype_id]
    url = "%s%s%s%s" % ("http://www.imdb.com/name/", imdb_id, "/#", type)
    print url
	
    try:
        body = get_url(url, cache=CACHE_PATH)
        try:
            all_tr = regex_get_all(body, '<div class="filmo-row', '</div>')
            for tr in all_tr:
                #all_td = regex_get_all(tr, '<div class="title">', '/div>')
                imdb_id = regex_from_to(all_tr, '/title/', '/')
                name = regex_from_to(all_tr, ';">', '</a')
                year = regex_from_to(all_tr, 'nbsp;', '</span>').replace("(","").replace(")","").strip()
                rating = ""
                votes = ""
                try:
                    exclude = regex_from_to(all_td[0], '</b>', '<br/>')
                except:
                    exclude = "AA"

                if exclude.find("(TV")<0 and exclude.find("(Shor")<0 and exclude.find("(Vid")<0:
                    movies.append({'imdb_id': imdb_id, 'name': name, 'year': year, 'rating': rating, 'votes': votes})
        except:
            xbmc.log("[What the Furk...XBMCHUB.COM] regex (name/filmotype) error")
            display_error("Unable to scrape imdb.com/name/filmoype", "Page structure may have changed")
    except:
        xbmc.log("[What the Furk...XBMCHUB.COM] IMDB name/filmotype URL request timed out")
        display_error("IMDB (name/filmotype) URL request timed out", "Is the website down?")
        movies.append({'imdb_id': "", 'name': "error", 'year': "visit www.xbmchub.com", 'rating': "", 'votes': ""})
    
    return create_movie_items(movies, start, name)
	
def nzbweek_menu():
    params = "Toplists/"
    movies = search_nzbmovie(params)
    return create_movie_items(movies,"","")
	
def nzbmonth_menu():
    params = "Toplists/Downloads/Month/"
    movies = search_nzbmovie(params)
    return create_movie_items(movies,"","")
	
def nzbyear_menu():
    params = "Toplists/Downloads/Year/"
    movies = search_nzbmovie(params)
    return create_movie_items(movies,"","")
	
def nzbwatchlist_menu():
    params = "Toplists/Watchlist/"
    movies = search_nzbmovie(params)
    return create_movie_items(movies,"","")
	
def watchlist_menu(start, name):
    params = {}
    nstart = str(int(start) + 250)
    params["title_type"] = "feature,documentary,tv_movie"
    params["start"] = start
    params["view"] = 'compact'
    url = "%s%s%s" % (IMDB_WATCHLIST, urllib.urlencode(params),"&sort=listorian:asc")
    movies = watchlist_imdb(url,start,name)
    return create_movie_items(movies, nstart, name)
	
def watchlist_tv_menu(start, name):
    params = {}
    nstart = str(int(start) + 250)
    params["title_type"] = "tv_series,mini_series,tv_special"
    params["start"] = start
    params["view"] = 'compact'
    url = "%s%s%s" % (IMDB_WATCHLIST, urllib.urlencode(params),"&sort=listorian:asc")
    tv_shows = watchlist_imdb(url,start,name)
    return create_tv_show_items(tv_shows, nstart, name)

					
def list1_menu():
    list = IMDB_LIST1
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list2_menu():
    list = {}
    list = IMDB_LIST2
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list3_menu():
    list = {}
    list = IMDB_LIST3
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list4_menu():
    list = {}
    list = IMDB_LIST4
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list5_menu():
    list = {}
    list = IMDB_LIST5
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list6_menu():
    list = {}
    list = IMDB_LIST6
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list7_menu():
    list = {}
    list = IMDB_LIST7
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list8_menu():
    list = {}
    list = IMDB_LIST8
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list9_menu():
    list = {}
    list = IMDB_LIST9
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def list10_menu():
    list = {}
    list = IMDB_LIST10
    movies = customlist_imdb(list)
    return create_movie_items(movies,"","")
	
def movies_mpaas_menu():
    items = []
    mpaas = ['G', 'PG', 'PG-13', 'R', 'NC-17']
    for mpaa in mpaas:
        items.append(create_movie_directory_tuple(mpaa, 'movie mpaa menu', '1'))
    return items

def movies_mpaa_menu(start, mpaa):
    mpaa1 = "%s%s" % ("us:",mpaa.lower().replace('-','_'))
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_MOV_MPAA
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["title_type"] = "feature,documentary,tv_movie"
    params["certificates"] = mpaa1
    params["production_status"] = PRODUCTION_STATUS
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    movies = search_imdb(url,start,mpaa)
    return create_movie_items(movies, nstart, mpaa)
	
def movies_genres_menu():
    items = []
    genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'History', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    for genre in genres:
        items.append(create_movie_directory_tuple(genre, 'movie genre menu', '1'))
    return items

def movies_genre_menu(start, genre):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_MOV_GEN
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["title_type"] = "feature,documentary,tv_movie"
    params["genres"] = genre
    params["production_status"] = PRODUCTION_STATUS
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    movies = search_imdb(url,start,genre)
    return create_movie_items(movies, nstart, genre)

def movies_groups_menu():
    items = []
    groups = ['Now Playing US', 'Oscar Winners', 'Oscar nominees', 'Oscar Best Picture Winners', 'Oscar Best Director Winners',
          'Golden Globe Winners', 'Golden Globe Nominees', 'National Film Registry', 'Razzie Winners', 'Top 100', 'Bottom 100']
    for group in groups:
        items.append(create_movie_directory_tuple(group, 'movie group menu', '1'))
    return items

def movies_group_menu(start, group):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_MOV_GRP
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["title_type"] = "feature,documentary,tv_movie"
    params["groups"] = group.replace(' ', '_')
    params["production_status"] = PRODUCTION_STATUS
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    movies = search_imdb(url,start,group)
    return create_movie_items(movies, nstart, group)

	
def movies_studios_menu():
    items = []
    studios = ['Columbia', 'Disney', 'Dreamworks', 'Fox', 'Mgm', 'Paramount', 'Universal', 'Warner']
    for studio in studios:
        items.append(create_movie_directory_tuple(studio, 'movie studio menu', '1'))
    return items

def movies_studio_menu(start, studio):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_MOV_STU
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["title_type"] = "feature,documentary,tv_movie"
    params["companies"] = studio
    params["production_status"] = PRODUCTION_STATUS
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    movies = search_imdb(url,start,studio)
    return create_movie_items(movies, nstart, studio)

def movies_new_menu(start, name):
    nstart = str(int(start) + IMDB_RESULTS)
    d = (date.today() - timedelta(days=NEWMOVIE_DAYS))
    params = {}
    params["release_date"] = "%s," % d
    params["sort"] = SORT_MOV_NEW
    params["title_type"] = "feature,documentary,tv_movie"
    params["num_votes"] = NUM_VOTES
    params["production_status"] = PRODUCTION_STATUS
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    movies = search_imdb(url,start,name)
    return create_movie_items(movies, nstart, name)
	
def movies_soon_menu(start, name):
    nstart = str(int(start) + IMDB_RESULTS)
    from_date = (date.today() + timedelta(1))
    to_date = (from_date + timedelta(30))
    params = {}
    params["release_date"] = "%s,%s" % (from_date, to_date)
    params["title_type"] = "feature,documentary,tv_movie"
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    movies = search_imdb(url,start,name)
    return create_movie_items(movies, nstart, name)
	
def blu_ray_menu(start, name):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_BLU_RAY
    params["title_type"] = "feature,documentary,tv_movie"
    params["has"] = "asin-blu-ray-us"
    params["production_status"] = PRODUCTION_STATUS
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    movies = search_imdb(url,start,name)
    return create_movie_items(movies, nstart, name)


def tv_shows_all_menu(start, name):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_TOP_TV
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    params["title_type"] = "tv_series,mini_series,tv_special"
    params["production_status"] = PRODUCTION_STATUS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    tv_shows = search_imdb(url,start,name)
    return create_tv_show_items(tv_shows, nstart, name)

def tv_shows_genres_menu():
    items = []
    genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'History', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    for genre in genres:
        items.append(create_movie_directory_tuple(genre, 'tv show genre menu', '1'))
    return items

def tv_shows_genre_menu(start,genre):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_TV_GEN
    params["title_type"] = "tv_series,mini_series,tv_special"
    params["genres"] = genre
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["production_status"] = PRODUCTION_STATUS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    tv_shows = search_imdb(url,start,genre)
    return create_tv_show_items(tv_shows, nstart, genre)
	
def tv_shows_groups_menu():
    items = []
    tvgroups = ['Emmy Winners', 'Emmy Nominees', 'Golden Globe Winners', 'Golden Globe Nominees']
    for tvgroup in tvgroups:
        items.append(create_movie_directory_tuple(tvgroup, 'tv show group menu', '1'))
    return items

def tv_shows_group_menu(start,tvgroup):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["release_date"] = RELEASE_DATE
    params["sort"] = SORT_TV_GRP
    params["title_type"] = "tv_series,mini_series,tv_special"
    params["groups"] = tvgroup.replace(' ', '_')
    params["num_votes"] = NUM_VOTES
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    params["user_rating"] = USER_RATING
    params["production_status"] = PRODUCTION_STATUS
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    tv_shows = search_imdb(url,start,tvgroup)
    return create_tv_show_items(tv_shows, nstart, tvgroup)

def tv_shows_active_menu(start, name):
    nstart = str(int(start) + IMDB_RESULTS)
    params = {}
    params["production_status"] = "active"
    params["num_votes"] = NUM_VOTES
    params["user_rating"] = USER_RATING
    params["sort"] = SORT_TV_ACT
    params["view"] = VIEW
    params["start"] = start
    params["count"] = IMDB_RESULTS
    params["title_type"] = "tv_series,mini_series,tv_special"
    url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
    tv_shows = search_imdb(url,start,name)
    return create_tv_show_items(tv_shows, nstart, name)
	
def tv_shows_seasons_menu(name, imdb_id):
    items = []
    info = TheTVDBInfo(imdb_id)
    episodes = info.episodes()
    
    seasons = set()
    
    for episode in episodes:
        first_aired = episode.FirstAired()
        if len(first_aired) > 0:
            d = first_aired.split('-')
            episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            if UNAIRED:
                season_number = int(episode.SeasonNumber())
                seasons.add(season_number)
            else:
                if date.today() > episode_date: #####removed to allow upcoming seasons
                    season_number = int(episode.SeasonNumber())
                    seasons.add(season_number)
                
    for season in sorted(seasons):
        if META_QUALITY == 'low':
            image_base_url = 'http://thetvdb.com/banners/seasons/_cache/'
        else:
            image_base_url = 'http://thetvdb.com/banners/seasons/'
        

        poster_href = str(info.id()) + "-" + str(season) + ".jpg"		
        poster = '%s%s' % (image_base_url, poster_href)

		
        if META_QUALITY == 'low':
            image_base_url = 'http://thetvdb.com/banners/_cache/'
        else:
            image_base_url = 'http://thetvdb.com/banners/'		
        fanart_href = info.fanart()
        if len(fanart_href) > 0:
            fanart = '%s%s' % (image_base_url, fanart_href)
		
        data = "%s<|>%d" % (name, season)
        season_tuple = create_season_tuple('Season %d' % season, data, imdb_id, poster, fanart)
        items.append(season_tuple)
        setView('movies', 'tvshows-view')
    return items;
    
def tv_shows_episodes_menu(data, imdb_id):
    items = []
    info = TheTVDBInfo(imdb_id)
    data_list = data.split("<|>")
    name = data_list[0]
    season = data_list[1]
    episodes = info.episodes()
    
    name = name.split('(')[0][:-1]
    
    for episode in episodes:
###########################################################################################################################################
        if META_QUALITY == 'low':
            image_base_url = 'http://thetvdb.com/banners/_cache/'
        else:
            image_base_url = 'http://thetvdb.com/banners/'
        poster_href = episode.filename()
        if len(poster_href) > 0:
            poster = '%s%s' % (image_base_url, poster_href)
        
        fanart_href = info.fanart()
        if len(fanart_href) > 0:
            fanart = '%s%s' % (image_base_url, fanart_href)
			
        title = episode.EpisodeName()
        year = episode.FirstAired().split('-')[0]
        overview = episode.Overview()
        if episode.Rating() == "":
            rating = 5.0
        else:
            rating = episode.Rating()
        premiered = episode.FirstAired()
        genre = info.Genre()

##########################################################################################################################################		
        first_aired = episode.FirstAired()
        if len(first_aired) > 0:
            d = first_aired.split('-')
            episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            if UNAIRED:
                season_number = int(episode.SeasonNumber())
                if season_number == int(season):
                    episode_number = int(episode.EpisodeNumber())
                    episode_name = episode.EpisodeName()
                    cleaned_name = clean_file_name(episode_name, use_blanks=False)
                    if date.today() > episode_date: #default text if episode has been aired
                        display = first_aired + ' - ' + "S%.2dE%.2d - %s" % (season_number, episode_number, cleaned_name)
                    elif date.today() == episode_date: #set orange font if air date is today
                        display = '[COLOR orange]' + first_aired + ' - ' + "S%.2dE%.2d - %s" % (season_number, episode_number, cleaned_name)+ '[/COLOR]'
                    elif date.today() < episode_date: #set red font if episode has not been aired
                        display = '[COLOR red]' + first_aired + ' - ' + "S%.2dE%.2d - %s" % (season_number, episode_number, cleaned_name)+ '[/COLOR]'
                    data = "%s<|>%s<|>%d<|>%d" % (name, episode_name, season_number, episode_number)
                    easyname = "S%.2d E%.2d %s" % (season_number, episode_number, name)
                    episode_tuple = create_episode_tuple(display, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname)
                    items.append(episode_tuple)
					
            else:
                if date.today() > episode_date:
                    season_number = int(episode.SeasonNumber())
                    if season_number == int(season):
                        episode_number = int(episode.EpisodeNumber())
                        episode_name = episode.EpisodeName()
                        cleaned_name = clean_file_name(episode_name, use_blanks=False)
                        display = "S%.2dE%.2d - %s" % (season_number, episode_number, cleaned_name)
                        data = "%s<|>%s<|>%d<|>%d" % (name, episode_name, season_number, episode_number)
                        easyname = "S%.2d E%.2d %s" % (season_number, episode_number, name)
                        episode_tuple = create_episode_tuple(display, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname)
                        items.append(episode_tuple)

    return items

def subscription_menu():
    if not os.path.isfile(SUBSCRIPTION_FILE):
        return main_menu()
    
    items = []
    s = read_from_file(SUBSCRIPTION_FILE)
    menu_items = s.split('\n')
    
    for menu_item in menu_items:
        if len(menu_item) < 3:
            break
        data = menu_item.split('\t')
        item_name = data[0]
        item_data = data[1]
        
        if item_data.startswith('tt'):
            items.append(create_tv_show_tuple(item_name, item_data,'',''))
        else:
            items.append(create_movie_directory_tuple(item_name, item_data, '1'))

    return items

def furk_search_menu():
    items = []
    items.append(create_directory_tuple('@Search...', 'furk result dialog menu'))
    
    if os.path.isfile(FURK_SEARCH_FILE):
        s = read_from_file(FURK_SEARCH_FILE)
        search_queries = s.split('\n')
        for query in search_queries:
            items.append(create_furk_search_tuple(query))

    return items

def imdb_search_menu():
    items = []
    items.append(create_directory_tuple('@Search...', 'imdb result menu'))
    
    if os.path.isfile(IMDB_SEARCH_FILE):
        s = read_from_file(IMDB_SEARCH_FILE)
        search_queries = s.split('\n')
        for query in search_queries:
            items.append(create_imdb_search_tuple(query))

    return items
	
def imdb_search_menu_tv():
    items = []
    items.append(create_directory_tuple('@Search...', 'imdb result tv menu'))
    
    if os.path.isfile(IMDB_SEARCH_FILE):
        s = read_from_file(IMDB_SEARCH_FILE)
        search_queries = s.split('\n')
        for query in search_queries:
            items.append(create_imdb_search_tuple_tv(query))

    return items
	
def imdb_actor_menu():
    items = []
    items.append(create_directory_tuple('@Search...', 'imdb actor result menu'))
    
    if os.path.isfile(IMDB_ACTOR_FILE):
        s = read_from_file(IMDB_ACTOR_FILE)
        search_queries = s.split('\n')
        for query in search_queries:
            items.append(create_imdb_actorsearch_tuple(query))

    return items
	
def download_movies_menu():
    items = []
    items.append(create_directory_tuple('[COLOR gold]' + ">> Refresh <<" + '[/COLOR]', 'refresh list'))
    
    if os.path.isfile(ACTIVE_DOWNLOADS):
        s = read_from_file(ACTIVE_DOWNLOADS)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = list[0]
                path = list[1]
                try:
                    size = list[2]
                    size_now = float(os.path.getsize(path))/1073741824
                    fmt_size = "%.2fGB" % float(size)
                    pct = round(100 * (float(size_now)/float(size)), 0)
                    if pct == 100:
                        pct = '[COLOR green]' + ("[%.0f%%/%s]" % (pct, fmt_size)) + '[/COLOR]'
                    else:
                        pct = '[COLOR yellow]' + ("[%.0f%%/%s]" % (pct, fmt_size)) + '[/COLOR]'
                except:
                    pct = '[COLOR green]' + ("[%.0f%%]" % (100.0/1)) + '[/COLOR]'
                    size = ""
                type = 'movie'
                items.append(create_download_file_tuple(name, path, type, pct, size))

    return items
	
def download_episodes_menu():
    items = []
    items.append(create_directory_tuple('[COLOR gold]' + ">> Refresh <<" + '[/COLOR]', 'refresh list'))
    
    if os.path.isfile(ACTIVE_DOWNLOADS_TV):
        s = read_from_file(ACTIVE_DOWNLOADS_TV)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = list[0]
                path = list[1]
                try:
                    size = list[2]
                    size_now = float(os.path.getsize(path))/1073741824
                    fmt_size = "%.2fGB" % float(size)
                    pct = round(100 * (float(size_now)/float(size)), 0)
                    if pct == 100:
                        pct = '[COLOR green]' + ("[%.0f%%/%s]" % (pct, fmt_size)) + '[/COLOR]'
                    else:
                        pct = '[COLOR yellow]' + ("[%.0f%%/%s]" % (pct, fmt_size)) + '[/COLOR]'
                except:
                    pct = '[COLOR green]' + ("[%.0f%%]" % (100.0/1)) + '[/COLOR]'
                    size = ""
                type = 'tv'
                items.append(create_download_file_tuple(name, path, type, pct, size))

    return items

def people_list_menu():
    items = []
    
    if os.path.isfile(PEOPLE_LIST):
        s = read_from_file(PEOPLE_LIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = list[0]
                imdb_id = list[1]
                photo = list[2]
                items.append(create_savedpeople_tuple(name, imdb_id, photo))

    return items
	
def wishlist_pending_menu():
    items = []
    
    if os.path.isfile(WISHLIST):
        s = read_from_file(WISHLIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = "%s | %s | %s" % (list[0], list[1], list[2])
                action = list[1]
                pct = ""
                type = 'movie'
                size = ""
                items.append(create_download_file_tuple(name, action, type, pct, size))

    return items
	
def wishlist_finished_menu():
    items = []
    
    if os.path.isfile(WISHLIST_FINISHED):
        s = read_from_file(WISHLIST_FINISHED)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                name = "%s | %s | %s" % (list[0], list[1], list[2])
                action = list[1]
                pct = ""
                type = 'movie'
                size = ""
                items.append(create_download_file_tuple(name, action, type, pct, size))

    return items
	
def delete_download(name, data, type):
    if type == "tv":
        data_path = os.path.join(DOWNLOAD_TV, name)
        download_list = ACTIVE_DOWNLOADS_TV
    else:
        data_path = os.path.join(DOWNLOAD_MOV, name)
        download_list = ACTIVE_DOWNLOADS
    list_data = "%s<|>%s<|>%s" % (name, data_path, data)
    print list_data
    print data_path
    if os.path.exists(data_path):
        try:
            os.remove(data_path)
            remove_search_query(list_data, download_list)
            xbmc.executebuiltin("Container.Refresh")
        except:
            print "Exception: ",str(sys.exc_info())
    else:
        print 'File not found at ',data
	
def xbmcplay(data):
    xbmc.Player().play(data)

def imdb_result_menu(query):
    if query.startswith('@'):
        query = ''
    
    keyboard = xbmc.Keyboard(query, 'Search', False)
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
			
        if len(query) > 0:
            add_search_query(query, IMDB_SEARCH_FILE)
            params = {}
            params["title"] = query
            dialog = xbmcgui.Dialog()
            params["title_type"] = "feature,documentary,tv_movie"
            params["view"] = VIEW
            params["start"] = "1"
            params["count"] = IMDB_RESULTS
            url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
            search_result = search_imdb(url,'1','search')
            setView('movies', 'movies-view')
            return create_movie_items(search_result,"","")

    return imdb_search_menu(), []
	
def imdb_result_menu_tv(query):
    if query.startswith('@'):
        query = ''
    
    keyboard = xbmc.Keyboard(query, 'Search', False)
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            add_search_query(query, IMDB_SEARCH_FILE)
            params = {}
            params["title"] = query
            dialog = xbmcgui.Dialog()
            params["view"] = VIEW
            params["start"] = "1"
            params["count"] = IMDB_RESULTS
            params["title_type"] = "tv_series,mini_series,tv_special"
            url = "%s%s" % (IMDB_TITLE_SEARCH, urllib.urlencode(params))
            search_result = search_imdb(url,'1','search')
            setView('movies', 'tvshows-view')
            return create_tv_show_items(search_result,"","")

    return imdb_search_menu_tv(), []
	
def imdb_actor_result_menu(query):
    if query.startswith('@'):
        query = ''
    
    keyboard = xbmc.Keyboard(query, 'Search People', False)
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            add_search_query(query, IMDB_ACTOR_FILE)
            params = {}
            params["name"] = query
            search_result = search_actors(params)
            setView('movies', 'movies-view')
            return create_actor_items(search_result)
 
    return imdb_actor_menu(), []
	
############################################### WTF BROWSE MEDIA ##############################################################
def episode_dialog(data, imdb_id, strm=False):################### SEARCH TV ARCHIVES ##########################################
    items = []
    dialog = xbmcgui.Dialog()
    data = data.replace('[COLOR cyan]','').replace('[/COLOR]','').replace('[COLOR gold]','')
    quality_list = ["Custom Search", "Season Search", "Any",  "1080P", "720P", "HDTV", "480P", "BDRIP", "BRRIP", "DVDRIP"]
    quality_list_return = ["Custom Search", "Season", "",  "1080P", "720P", "HDTV", "480P", "BDRIP", "BRRIP", "DVDRIP"]
	
    if re.search('<|>',data):
        data = data.split('<|>')
    else:
        if re.search('$',data):
            data = data.split('$')
    tv_show_name = data[0].replace(" Mini-Series","").replace("The ","")
    episode_name = data[1]
    season_number = int(data[2])
    episode_number = int(data[3])

    season_episode = "s%.2de%.2d" % (season_number, episode_number)
    season_episode2 = "%s %dx%.2d" % (tv_show_name, season_number, episode_number)
    season_episode3 = "%s season %d" % (tv_show_name, season_number)

    tv_show_season = "%s season" % (tv_show_name)
    tv_show_episode = "%s %s" % (tv_show_name, season_episode)
    track_filter = [episode_name, season_episode, season_episode2]
	
    if not login_at_furk():
        return []
    xbmcname = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))	
    files = []
  
    if FURK_SEARCH_MF:
        try:
            tv_show = tv_show_name.lower().split(' ')
            mfiles = []
            my_files = FURK.file_get('0')
            mfiles = my_files.files
            for f in mfiles:
                if (tv_show_name.find(' ')>0 and tv_show[0] in f.name.lower() and tv_show[1] in f.name.lower()) or (tv_show_name in f.name.lower()):
                    count_files = (f.files_num_video)
                    name = f.name
                    url = f.url_dl
                    id = f.id
                    size = f.size
                    size = float(size)/1073741824
                    size = "[%.2fGB]" % size
                    text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                    try:
                        poster = f.ss_urls_tn[0]
                    except:
                        poster = ""
                    xbmcname = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))

                    mode = "t files menu"
                    archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, "", "tv")
                    items.append(archive_tuple)
        except:
            pass
        time.sleep(F_DELAY)

    if QUALITYSTYLE_TV == "preferred":
        operator="%7C"
        searchstring = "%s %s %s %s" % (tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "), TVCUSTOMQUALITY, operator, TVCUSTOMQUALITY2)
        files = search_furk(searchstring, "extended")
        count=0
        for f in files:
            if f.is_ready == "0":
                count=count+1
        if (count == len(files) and len(files)>0) or len(files)==0:
            time.sleep(F_DELAY)
            notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
            xbmc.executebuiltin(notify)
            searchstring = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))
            files.extend(search_furk(searchstring, "all"))
    else:
        quality_id = dialog.select("Select your preferred option", quality_list)
        quality = quality_list_return[quality_id]
    
        if(quality_id == 0):
            searchstring = tv_show_name
            keyboard = xbmc.Keyboard(searchstring, 'Custom Search', False)
            keyboard.doModal()
            if keyboard.isConfirmed():
                searchstring = keyboard.getText()
        elif(quality_id == 2):
            searchstring = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))
        elif(quality_id == 1):
            searchstring = str(season_episode3)
        else:            
            searchstring = "%s %s" % (tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "), quality)
        if(quality_id < 0):
            return (None, None)
            dialog.close()
        files = search_furk(searchstring, "all")

    if len(files) == 0:
        if dialog.yesno("File Search", 'No files found for:', searchstring.replace('%7C','|'), "Search latest torrents?"):
            download_kat(tv_show_name, season_episode)
            return (None, None)
        else:
            return (None, None)
		
    if FURK_LIM_FS_TV:
        fs_limit = FURK_LIM_FS_NUM_TV
    else:
        fs_limit = 50
    for f in files:
        if len(f.name) > 0 and float(f.size)/1073741824 < fs_limit:
            name = f.name.encode('utf-8','ignore')
            url = f.url_dl
            id = f.id
            video_info = f.video_info
            
            try:
                match = re.compile('Duration: (.+?), start: (.+?),').findall(video_info)
                for duration, start in match:
                    duration = duration.split('.')
                    length = duration[0]
                    timestr = duration[0]
                    ftr = [3600,60,1]
                    duration = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                match2 = re.compile('bitrate: (.+?) ').findall(video_info)
                match1 = re.compile('Video: (.+?), (.+?), (.+?),').findall(video_info.replace('[',''))
            
                for format, color, vid_info in match1:
                    vid_info = "%s %s" % (format, vid_info)
                for bitrate in match2:
                    br = bitrate.replace('kb/s','')
            except:
                duration=""
                br=1
                vid_info=""
            is_ready = f.is_ready
            info_hash = f.info_hash
            size = f.size
            try:
                bitrate = float(size)/duration*8/1024/1024
            except:
                try:
                    bitrate = float(br)
                except:
                     bitrate = 5
            if bitrate < float(DOWNLOAD_SPEED):
                bitrate = "[COLOR lime][%.1fMbps][/COLOR]" % (bitrate)
            else:
                bitrate = "[COLOR orange][%.1fMbps][/COLOR]" % (bitrate)
            size = float(size)/1073741824
            size = "[%.2fGB]" % size
            text = "%s %s %s" %(size, name, bitrate)
            if  is_ready == "1" and f.type == "video" and f.url_dl != None:
                if QUALITYSTYLE_TV == "preferred" or quality_id > 1:
                    text = "[COLOR gold]%s[/COLOR] %s [COLOR cyan]%s[/COLOR] info: %s %s" %(size, bitrate, name, length, vid_info)
                else:
                    text = "[COLOR gold]%s[/COLOR] [COLOR cyan]%s[/COLOR]" %(size, name)
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                mode = "t files tv menu"
                type = "tv"
            else:
                text = '[COLOR red]' + "%s %s" %(size, name)+ '[/COLOR]'
                poster = ""
                id = info_hash
                mode = "add download"
                type = "tv"

            archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, imdb_id,type)
            items.append(archive_tuple)
            setView('movies', 'movies-view')

    return items;

def movie_dialog(data, imdb_id, strm=False):################### SEARCH MOVIE ARCHIVES ##########################################
    items = []
    if FURK_SEARCH_MF:
        try:
            if mode=="music video menu":
                name2 = data
            else:
                name2 = data[:len(data)-7].replace("The ","").lower()
            mfiles = []
            my_files = FURK.file_get('0')
            mfiles = my_files.files
            name3 = name2.split(' ')
            for f in mfiles:
                if (name2.find(' ')>0 and name3[0] in f.name.lower() and name3[1] in f.name.lower()) or (name2 in f.name.lower()):
                    count_files = (f.files_num_video)
                    name = f.name
                    url = f.url_dl
                    id = f.id
                    size = f.size
                    size = float(size)/1073741824
                    size = "[%.2fGB]" % size
                    text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                    try:
                        poster = f.ss_urls_tn[0]
                    except:
                        poster = ""
                    xbmcname = str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," "))

                    mode1 = "t files menu"
                    archive_tuple = create_archive_tuple(xbmcname, text, name, mode1, url, str(id), size, poster, "", "movie")
                    items.append(archive_tuple)
        except:
            pass
        time.sleep(F_DELAY)
		
    files = []
        
    dialog = xbmcgui.Dialog()
    quality_list = ["Any", "3D", "1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
    quality_list_return = ["", "3D","1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]

    if QUALITYSTYLE == "preferred" or ' 3D' in data:
        operator="%7C"
        if ' 3D' in data:
            searchstring = str(data.replace(",","").replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ").replace("(","").replace(")",""))
        elif mode=="music video menu":
            searchstring = str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ").replace("(","").replace(")",""))
        else:
            searchstring = "%s %s %s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ").replace("(","").replace(")","")), str(CUSTOMQUALITY), str(operator), str(CUSTOMQUALITY2))
        files = search_furk(searchstring, "extended")
        count=0
        for f in files:
            if f.is_ready == "0":
                count=count+1
        if (count == len(files) and len(files)>0) or len(files)==0:
            time.sleep(F_DELAY)
            notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
            xbmc.executebuiltin(notify)
            files.extend(search_furk(str(data.replace("-","").replace(" Documentary","").replace(" TV Movie","").replace(":","").replace("(","").replace(")","")), "all"))
    else:
        quality_id = dialog.select("Select your preferred option", quality_list)
        quality = quality_list_return[quality_id]
        if(quality_id < 0):
            return (None, None)
            dialog.close()
        if(quality_id == 0):
            searchstring = str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ").replace("(","").replace(")",""))
        else:
            searchstring = "%s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ").replace("(","").replace(")","")), quality)
        files = search_furk(searchstring, "all")
    xbmcname = str(data.replace("-"," ").replace(" Documentary","").replace(":"," "))
    if len(files) == 0:
        if dialog.yesno("File Search", 'No files found for:', searchstring.replace('%7C','|'), "Search latest torrents?"):
            download_kat(str(data.replace("-"," ").replace(" Documentary","").replace(":"," ")), "dummy")
            return (None, None)
        else:
            return (None, None)

    if FURK_LIM_FS:
        fs_limit = FURK_LIM_FS_NUM
    else:
        fs_limit = 100
    for f in files:
        if float(f.size)/1073741824 < fs_limit and ((f.type == "video" and f.video_info.find("mpeg2video")<0) or f.is_ready =="0"):
            name = f.name.encode('utf-8','ignore')
            url = f.url_dl
            id = f.id
            video_info = f.video_info
            match = re.compile('Duration: (.+?), start: (.+?),').findall(video_info)
            match2 = re.compile('bitrate: (.+?) ').findall(video_info)
            match1 = re.compile('Video: (.+?), (.+?), (.+?),').findall(video_info.replace('[',''))
            for duration, start in match:
                duration = duration.split('.')
                length = duration[0]
                timestr = duration[0]
                ftr = [3600,60,1]
                duration = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
            for format, color, vid_info in match1:
                vid_info = "%s %s" % (format, vid_info)
            for bitrate in match2:
                br = bitrate
            is_ready = f.is_ready
            info_hash = f.info_hash
            size = f.size
            try:
                bitrate = float(size)/duration*8/1024/1024
            except:
                bitrate = 2
            if bitrate < float(DOWNLOAD_SPEED):
                bitrate = "[COLOR lime][%.1fMbps][/COLOR]" % (bitrate)
            else:
                bitrate = "[COLOR orange][%.1fMbps][/COLOR]" % (bitrate)
            size = float(size)/1073741824
            size = "[%.2fGB]" % size
            if  is_ready == "1" and f.type == "video" and f.url_dl != None:
                text = "[COLOR gold]%s[/COLOR] %s [COLOR cyan]%s[/COLOR] info: %s %s" %(size, bitrate, name, length, vid_info)
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                if mode == "music video menu":
                    mode1 = "t music vid files menu"
                else:
                    mode1 = "t files menu"
            else:
                text = '[COLOR red]' + "%s %s" %(size, name)+ '[/COLOR]'
                poster = ""
                id = info_hash
                mode1 = "add download"
            archive_tuple = create_archive_tuple(xbmcname, text, name, mode1, url, str(id), size, poster, imdb_id, "movie")
            items.append(archive_tuple)
            setView('movies', 'movies-view')
		
    return items;
	
def furksearch_dialog(query, imdb_id=None, strm=False):############# FURK SEARCH #############
    items = []	
    files = []
    if query.startswith('@'):
        query = ''
    
    keyboard = xbmc.Keyboard(query, 'Search', False)
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            add_search_query(query, FURK_SEARCH_FILE)
            files = search_furk(str(query), "all")
    xbmcname = str(query)
	
    if FURK_SEARCH_MF:
        try:
            name2 = query[:len(query)-7].replace("The ","").lower()
            mfiles = []
            my_files = FURK.file_get('0')
            mfiles = my_files.files
            name3 = name2.split(' ')
            for f in mfiles:
                if (name2.find(' ')>0 and name3[0] in f.name.lower() and name3[1] in f.name.lower()) or (name2 in f.name.lower()):
                    count_files = (f.files_num_video)
                    name = f.name
                    url = f.url_dl
                    id = f.id
                    size = f.size
                    size = float(size)/1073741824
                    size = "[%.2fGB]" % size
                    text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                    try:
                        poster = f.ss_urls_tn[0]
                    except:
                        poster = ""
                    xbmcname = f.name

                    mode = "t files menu"
                    archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, "", "movie")
                    items.append(archive_tuple)
        except:
            pass
        time.sleep(F_DELAY)
	
    if len(files) == 0:
        dialog.ok("File Search", 'No files found for:', query) 

    for f in files:
        if f.type == "video" and f.video_info.find("mpeg2video")<0:
            name = f.name.encode('utf-8','ignore')
            url = f.url_dl
            id = f.id
            is_ready = f.is_ready
            info_hash = f.info_hash
            video_info = f.video_info
            match = re.compile('Duration: (.+?), start: (.+?),').findall(video_info)
            match2 = re.compile('bitrate: (.+?) ').findall(video_info)
            match1 = re.compile('Video: (.+?), (.+?), (.+?),').findall(video_info.replace('[',''))
            for duration, start in match:
                duration = duration.split('.')
                length = duration[0]
                timestr = duration[0]
                ftr = [3600,60,1]
                duration = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
            for format, color, vid_info in match1:
                vid_info = "%s %s" % (format, vid_info)
            for bitrate in match2:
                br = bitrate
            size = f.size
            bitrate = float(size)/duration*8/1024/1024
            if bitrate < float(DOWNLOAD_SPEED):
                bitrate = "[COLOR lime][%.1fMbps][/COLOR]" % (bitrate)
            else:
                bitrate = "[COLOR orange][%.1fMbps][/COLOR]" % (bitrate)
            size = float(size)/1073741824
            size = "[%.2fGB]" % size
            if  is_ready == "1" and f.type == "video" and f.url_dl != None:
                text = "[COLOR gold]%s[/COLOR] %s [COLOR cyan]%s[/COLOR] info: %s %s" %(size, bitrate, name, length, vid_info)
                try:
                    poster = f.ss_urls_tn[0]
                except:
                    poster = ""
                mode = "t files menu"
            else:
                text = '[COLOR red]' + "%s %s" %(size, name)+ '[/COLOR]'
                poster = os.path.join(ADDON.getAddonInfo('path'),'art','noentry.png')
                id = info_hash
                mode = "add download"

            archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster,"", "movie")
            items.append(archive_tuple)
            setView('movies', 'movies-view')
    return items;
	
def t_file_dialog_movie(xbmcname, id, imdb_id, strm=False):################### EXPLORE T FILES ##########################################
    items = []
    files = []
    if os.path.exists(TEMP_PATH):
        os.remove(TEMP_PATH)
    if mode == "t files menu" or mode == "t music files menu" or mode == "browse context menu":
        type = "movie"
        view = "movies-view"
    elif mode == "t music vid files menu":
        type = "musicvid"
        view = "movies-view"
    else:
        type = "tv"
        view = "tvshows-view"

    dialog = xbmcgui.Dialog()
    my_files = FURK.t_file_get(id, t_files="1")
    files = my_files.files

    for f in files:
        video = int(f.files_num_video)
        try:
            poster = f.ss_urls_tn[0]
        except:
            poster = ""
        t_files = f.t_files

    all_tf = regex_get_all(str(t_files), "{", "'}")
    count=0
    for tf in all_tf:
        all_td = regex_get_all(tf, "{", "'}")
        name = regex_from_to(str(all_td), "name': u'", "', u")
        format = name[len(name)-3:]
        url = regex_from_to(str(all_td), "url_dl': u'", "', u")
        duration = regex_from_to(str(all_td), "u'length': u'", "',")
        size = regex_from_to(str(all_td), "size': u'", "'")
        if duration == "0":
            bitrate = 5
            MBs = bitrate/8
        else:
            bitrate = float(size)/float(duration)*8/1024/1024
            MBs = bitrate/8
        if bitrate < float(DOWNLOAD_SPEED):
            bitrate = "[COLOR lime][%.1fMbps][/COLOR]" % (bitrate)
        else:
            bitrate = "[COLOR orange][%.1fMbps][/COLOR]" % (bitrate)
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        content = regex_from_to(str(all_td), "u'ct': u'", "/")
        text = "[%s] %s %s %s" %(format, size, name, bitrate)
      
	
        if mode == "t music files menu":
            wtf_mode = "execute video"
            file_list_tuple = create_file_list_tuple(xbmcname, text, name, wtf_mode, url, size, poster, type, imdb_id)
            items.append(file_list_tuple)
            setView('movies', view)
        elif name.lower().find('sample')<0 and (content == "video" or (name.endswith('srt') and DOWNLOAD_SUB)):
            if DPD:
                wtf_mode = "download play delete"
                imdb_id="%s$%s$%s" % ("down_delete", MBs, imdb_id)
                type = format
            else:
                wtf_mode = "execute video"
                #imdb = imdb_id
                imdb_id="%s$%s$%s" % (type, MBs, imdb_id)
            file_list_tuple = create_file_list_tuple(xbmcname, text, name, wtf_mode, url, size, poster, type, imdb_id)
            items.append(file_list_tuple)
            if content=="video" and SKIP_BROWSE and mode != "browse context menu":
                count+=1
                xn=xbmcname
                n=name
                u=url
                i = imdb_id
                isplit = imdb_id.split("$")
                imbd=isplit[2]
                f = format
                
            setView('movies', view)
    if count==1 and mode != "browse context menu":
        if LIBRARY_FORMAT:
            if DPD:
                download_play("%s.%s" % (xn,f), u, imdb_id)
            else:
                execute_video(xn, u, imbd, strm=False)
        else:
            if DPD:
                download_play(n, u, imdb_id)
            else:
                execute_video(n, u, imbd, strm=False)
            
    return items;
   
    	
############################################### END BROWSE MEDIA #########################################################################

############################################### STREAM FROM XBMC LIBRARY ##############################################################	
def strm_episode_dialog(data, imdb_id, strm=False):##################### SEARCH EPISODES ##########################
    menu_texts = []
    menu_data = []
    menu_linkid = []
    menu_url_pls = []
    customstring="abcdef"
	
    if ONECLICK_SEARCH:
        one_click_episode(data, imdb_id, strm=True)
    else:
        dialog = xbmcgui.Dialog()
        quality_list = ["Custom Search", "Season Search", "Any",  "1080P", "720P", "HDTV", "480P", "BDRIP", "BRRIP", "DVDRIP"]
        quality_list_return = ["Custom Search", "Season", "",  "1080P", "720P", "HDTV", "480P", "BDRIP", "BRRIP", "DVDRIP"]
	
        if re.search('<|>',data):
            data = data.split('<|>')
        else:
            if re.search('$',data):
                data = data.split('$')
        tv_show_name = data[0].replace(" Mini-Series","").replace("The ","")
        episode_name = data[1]
        season_number = int(data[2])
        episode_number = int(data[3])

        season_episode = "s%.2de%.2d" % (season_number, episode_number)
        season_episode2 = "%s %dx%.2d" % (tv_show_name, season_number, episode_number)
        season_episode3 = "%s season %d" % (tv_show_name, season_number)
        easyname = "S%.2d E%.2d %s" % (season_number, episode_number, tv_show_name)
        blank = None
        fanart = None
        description = None

        tv_show_season = "%s season" % (tv_show_name)
        tv_show_episode = "%s %s" % (tv_show_name, season_episode)
        track_filter = [episode_name, season_episode, season_episode2]
	
        if not login_at_furk():
            return []
			
        if FURK_SEARCH_MF:
            try:
                tv_show = tv_show_name.lower().split(' ')
                mfiles = []
                my_files = FURK.file_get('0')
                mfiles = my_files.files
                for f in mfiles:
                    if (tv_show_name.find(' ')>0 and tv_show[0] in f.name.lower() and tv_show[1] in f.name.lower()) or (tv_show_name in f.name.lower()):
                        count_files = (f.files_num_video)
                        name = f.name
                        size = f.size
                        size = float(size)/1073741824
                        size = "[%.2fGB]" % size
                        text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                        menu_texts.append(text)
                        menu_data.append(f.url_dl)
                        menu_linkid.append(f.id)
                        menu_url_pls.append(f.url_pls)
            except:
                pass
            time.sleep(F_DELAY)
	
        files = []

        if QUALITYSTYLE_TV == "preferred":
            operator="%7C"
            searchstring = "%s %s %s %s" % (tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "), TVCUSTOMQUALITY, operator, TVCUSTOMQUALITY2)
            files = search_furk(searchstring, "extended")
            count=0
            for f in files:
                if f.is_ready == "0":
                    count=count+1
            if (count == len(files) and len(files)>0) or len(files)==0:
                time.sleep(F_DELAY)
                notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
                xbmc.executebuiltin(notify)
                searchstring = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":"," "))
                files.extend(search_furk(searchstring, "all"))
        else:
            quality_id = dialog.select("Select your preferred option", quality_list)
            quality = quality_list_return[quality_id]
    
            if(quality_id == 0):
                searchstring = tv_show_name
                keyboard = xbmc.Keyboard(searchstring, 'Custom Search', False)
                keyboard.doModal()
                if keyboard.isConfirmed():
                    searchstring = keyboard.getText()
                    customstring=searchstring
            elif(quality_id == 2):
                searchstring = str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":",""))
            elif(quality_id == 1):
                searchstring = str(season_episode3)
            else:            
                searchstring = "%s %s" % (tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":",""), quality)
            if(quality_id < 0):
                return (None, None)
                dialog.close()
            files = search_furk(searchstring, "all")

        if QUALITYSTYLE_TV == "preferred" or (FURK_LIM_FS_TV and (quality_id != 1)):
            fs_limit = FURK_LIM_FS_NUM_TV
        else:
            fs_limit = 50
        for f in files:
            if f.type == "video" and f.url_dl != None and float(f.size)/1073741824 < fs_limit:
                name = f.name
                size = f.size
                is_ready = f.is_ready
                video_info = f.video_info
                match = re.compile('Duration: (.+?), start: (.+?),').findall(video_info)
                match2 = re.compile('bitrate: (.+?) ').findall(video_info)
                match1 = re.compile('Video: (.+?), (.+?), (.+?),').findall(video_info.replace('[',''))
                for duration, start in match:
                    duration = duration.split('.')
                    length = duration[0]
                    timestr = duration[0]
                    ftr = [3600,60,1]
                    duration = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                for format, color, vid_info in match1:
                    vid_info = "%s %s" % (format, vid_info)
                for bitrate in match2:
                    br = bitrate
                bitrate = float(size)/duration*8/1024/1024
                if bitrate < float(DOWNLOAD_SPEED):
                    bitrate = "[COLOR lime][%.1fMbps][/COLOR]" % (bitrate)
                else:
                    bitrate = "[COLOR orange][%.1fMbps][/COLOR]" % (bitrate)
                size = float(size)/1073741824
                size = "[%.2fGB]" % size
                if  is_ready == "1" and f.type == "video" and f.url_dl != None:
                    if QUALITYSTYLE_TV == "preferred" or quality_id > 1:
                        text = "[COLOR gold]%s[/COLOR] %s [COLOR cyan]%s[/COLOR] info: %s %s" %(size, bitrate, name, length, vid_info)
                    else:
                        text = "[COLOR gold]%s[/COLOR] [COLOR cyan]%s[/COLOR]" %(size, name)
                menu_texts.append(text)
                menu_data.append(f.url_dl)
                menu_linkid.append(f.id)
                menu_url_pls.append(f.url_pls)
				
        menu_texts.append("...Search 1Channel")
        menu_texts.append("...Search Icefilms")
        menu_texts.append("...Search MovieStorm")
        menu_texts.append("...Search TVonline")
        menu_texts.append("...Search TV4ME")
        menu_texts.append("...Search latest torrents")

        menu_id = dialog.select('Select Archive', menu_texts)
        iname = "%s %sx%.2d" % (tv_show_name,season_number,episode_number)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        if customstring!="abcdef":
            easyname=customstring
            tv_show_name=customstring
            iname=customstring
        if(menu_id == len(menu_texts)-6):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
                xbmc.executebuiltin(('Container.Update(%s?mode=7000&section=tv&query=%s)' %('plugin://plugin.video.1channel/',tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the 1Channel addon to use this function")
        elif(menu_id == len(menu_texts)-5):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
                iurl='http%3a%2f%2fwww.icefilms.info%2f'
                xbmc.executebuiltin(('Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',iurl,urllib.quote(iname),"0")))
            else:
                dialog.ok("Addon not installed", "", "Install the Icefilms addon to use this function")
        elif(menu_id == len(menu_texts)-4):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.moviestorm'):
                xbmc.executebuiltin(('Container.Update(%s?mode=7&url=%s&name=%s)' %('plugin://plugin.video.moviestorm/',"url", tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the MovieStorm addon to use this function")
        elif(menu_id == len(menu_texts)-3):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.tvonline.cc'):
                xbmc.executebuiltin(('Container.Update(%s?mode=17&url=%s&name=%s)' %('plugin://plugin.video.tvonline.cc/',"url", tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the TVonline addon to use this function")
        elif(menu_id == len(menu_texts)-2):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.tv4me'):
                xbmc.executebuiltin(('Container.Update(%s?mode=18&url=%s&name=%s)' %('plugin://plugin.video.tv4me/',"url", tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the TV4ME addon to use this function")
        elif(menu_id == len(menu_texts)-1):
            download_kat(tv_show_name, season_episode)
        else:
            id = str(menu_linkid[menu_id])
            t_file_dialog(id, imdb_id, tv_show_episode)

def strm_movie_dialog(name, imdb_id, strm=False):##################### SEARCH MOVIES ##########################
    open_playlists = True
    menu_texts = []
    menu_data = []
    menu_linkid = []
    menu_url_pls = []
    name2 = name[:len(data)-7].replace("The ","").lower()
    filename=name
    customstring="abcdef"
		
    if ONECLICK_SEARCH:
        one_click_movie(name, imdb_id, strm=True)

    else:
        if FURK_SEARCH_MF:
            try:
                name3 = name2.split(' ')
                mfiles = []
                my_files = FURK.file_get('0')
                mfiles = my_files.files
                for f in mfiles:
                    if (name2.find(' ')>0 and name3[0] in f.name.lower() and name3[1] in f.name.lower()) or (name2 in f.name.lower()):
                        count_files = (f.files_num_video)
                        name = f.name
                        size = f.size
                        size = float(size)/1073741824
                        size = "[%.2fGB]" % size
                        text = '[COLOR gold]' + "%s %s %s [%s files]" %("MF:",size, f.name, count_files) + '[/COLOR]'
                        menu_texts.append(text)
                        menu_data.append(f.url_dl)
                        menu_linkid.append(f.id)
                        menu_url_pls.append(f.url_pls)
            except:
                pass
            time.sleep(F_DELAY)
					
        dialog = xbmcgui.Dialog()
        quality_list = ["Custom Search", "Any", "3D", "1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
        quality_list_return = ["Custom","", "3D", "1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
	
        if not login_at_furk():
            return []
		
        files = []
        if QUALITYSTYLE == "preferred":
            operator="%7C"
            searchstring = "%s %s %s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ")), CUSTOMQUALITY, operator, CUSTOMQUALITY2)
            files = search_furk(searchstring, "extended")
            count=0
            for f in files:
                if f.is_ready == "0":
                    count=count+1
            if (count == len(files) and len(files)>0) or len(files)==0:
                time.sleep(F_DELAY)
                notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
                xbmc.executebuiltin(notify)
                files.extend(search_furk(str(data.replace("-","").replace(" Documentary","").replace(" TV Movie","").replace(":","")), "all"))
        else:		
            quality_id = dialog.select("Select your preferred option", quality_list)
            quality = quality_list_return[quality_id]
            if(quality_id < 0):
                return (None, None)
                dialog.close()
            if(quality_id == 0):
                searchstring = str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ").replace("(","").replace(")",""))
                keyboard = xbmc.Keyboard(searchstring, 'Custom Search', False)
                keyboard.doModal()
                if keyboard.isConfirmed():
                    searchstring = keyboard.getText()
                    customstring=searchstring
            elif(quality_id == 1):
                searchstring = str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ").replace("(","").replace(")",""))
            else:
                searchstring = "%s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ").replace("(","").replace(")","")), quality)
            files = search_furk(searchstring, "all")
    
        if FURK_LIM_FS:
            fs_limit = FURK_LIM_FS_NUM
        else:
            fs_limit = 50
        for f in files:
            if f.type == "video" and f.url_dl != None and float(f.size)/1073741824 < fs_limit:
                name = f.name
                size = f.size
                is_ready = f.is_ready
                video_info = f.video_info
                match = re.compile('Duration: (.+?), start: (.+?),').findall(video_info)
                match2 = re.compile('bitrate: (.+?) ').findall(video_info)
                match1 = re.compile('Video: (.+?), (.+?), (.+?),').findall(video_info.replace('[',''))
                for duration, start in match:
                    duration = duration.split('.')
                    length = duration[0]
                    timestr = duration[0]
                    ftr = [3600,60,1]
                    duration = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                for format, color, vid_info in match1:
                    vid_info = "%s %s" % (format, vid_info)
                for bitrate in match2:
                    br = bitrate
                bitrate = float(size)/duration*8/1024/1024
                if bitrate < float(DOWNLOAD_SPEED):
                    bitrate = "[COLOR lime][%.1fMbps][/COLOR]" % (bitrate)
                else:
                    bitrate = "[COLOR orange][%.1fMbps][/COLOR]" % (bitrate)
                size = float(size)/1073741824
                size = "[%.2fGB]" % size
                if  is_ready == "1" and f.type == "video" and f.url_dl != None:
                    if QUALITYSTYLE == "preferred" or quality_id > 0:
                        text = "[COLOR gold]%s[/COLOR] %s [COLOR cyan]%s[/COLOR] info: %s %s" %(size, bitrate, name, length, vid_info)
                    else:
                        text = "[COLOR gold]%s[/COLOR] [COLOR cyan]%s[/COLOR]" %(size, name)
                menu_texts.append(text)
                menu_data.append(f.url_dl)
                menu_linkid.append(f.id)
                menu_url_pls.append(f.url_pls)

        menu_texts.append("...Search yify Movies HD")				
        menu_texts.append("...Search 1Channel")
        menu_texts.append("...Search Icefilms")
        menu_texts.append("...Search MovieStorm")
        menu_texts.append("...Search latest torrents")

        menu_id = dialog.select('Select Archive', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        if customstring!="abcdef":
            name=customstring
            name2=customstring
        if(menu_id == len(menu_texts)-5):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.yifymovies.hd'):
                name2 = name[:len(data)-7].replace("The ","")        
                xbmc.executebuiltin(('XBMC.Container.Update(%s?action=movies_search&query=%s)' %('plugin://plugin.video.yifymovies.hd/',urllib.quote_plus(name2))))
            else:
                dialog.ok("Addon not installed", "", "Install the yify Movies HD addon to use this function")
        elif(menu_id == len(menu_texts)-4):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
                xbmc.executebuiltin(('Container.Update(%s?mode=7000&section=&query=%s)' %('plugin://plugin.video.1channel/',name2)))
            else:
                dialog.ok("Addon not installed", "", "Install the 1Channel addon to use this function")
        elif(menu_id == len(menu_texts)-3):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
                url='http%3a%2f%2fwww.icefilms.info%2f'
                xbmc.executebuiltin(('Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',url,urllib.quote_plus(name2),"0")))
            else:
                dialog.ok("Addon not installed", "", "Install the IceFilms addon to use this function")
        elif(menu_id == len(menu_texts)-2):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.moviestorm'):
                url='http%3a%2f%2fwww.icefilms.info%2f'
                xbmc.executebuiltin(('Container.Update(%s?mode=7&url=%s&name=%s)' %('plugin://plugin.video.moviestorm/',"url",name2)))
            else:
                dialog.ok("Addon not installed", "", "Install the MovieStorm addon to use this function")
        elif(menu_id == len(menu_texts)-1):
            download_kat(str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ")), "dummy")
        else:
            id = str(menu_linkid[menu_id])
            t_file_dialog(id, imdb_id, filename)
			
def t_file_dialog(id, imdb_id, filename, strm=True):################### T FILES ################################
    menu_texts = []
    menu_data = []
    menu_size = []
    menu_list_item = []
    files = []
    dialog = xbmcgui.Dialog()
    my_files = FURK.t_file_get(id, t_files="1")
    files = my_files.files
    for f in files:
        t_files = f.t_files
    all_tf = regex_get_all(str(t_files), "{", "'}")
    for tf in all_tf:
        all_td = regex_get_all(tf, "{", "'}")
        try:
            name = regex_from_to(str(all_td), "name': u'", "', u")
        except:
            name = "file.avi"
        format = name[len(name)-3:]
        url = regex_from_to(str(all_td), "url_dl': u'", "', u")
        size = regex_from_to(str(all_td), "size': u'", "'")
        content = regex_from_to(str(all_td), "u'ct': u'", "/")
        duration = regex_from_to(str(all_td), "u'length': u'", "',")
        if duration == "0":
            bitrate = 5
            MBs = bitrate/8
        else:
            bitrate = float(size)/float(duration)*8/1024/1024
            MBs = bitrate/8
        if bitrate < float(DOWNLOAD_SPEED):
            bitrate = "[COLOR lime][%.1fMbps][/COLOR]" % (bitrate)
        else:
            bitrate = "[COLOR orange][%.1fMbps][/COLOR]" % (bitrate)
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        i="%s$%s$%s" % ("down_delete", MBs, imdb_id)
        content = regex_from_to(str(all_td), "u'ct': u'", "/")
        text = "[%s] %s %s %s" %(format, size, name, bitrate)
        if name.lower().find('sample')<0 and content == "video":
            menu_texts.append(text)
            menu_list_item.append(name)
            menu_data.append(url)
            menu_size.append(size)
    if len(menu_texts)==1 and SKIP_BROWSE:
        menu_id=0
        url = menu_data[menu_id]
        name = menu_list_item[menu_id]
        format = name[len(name)-3:]
        list_item = menu_list_item[menu_id]
        if not url or not name:
            if strm:
                set_resolved_to_dummy()
            return
    
        li = xbmcgui.ListItem(list_item)
        if LIBRARY_FORMAT:
            execute_video(filename, url, imdb_id, strm)
        else:
            execute_video(name, url, imdb_id, strm)

    else:			
        menu_id = dialog.select('Select file', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        else:	
            url = menu_data[menu_id]
            name = menu_list_item[menu_id]
            format = name[len(name)-3:]
            list_item = menu_list_item[menu_id]
    
            if not url or not name:
                if strm:
                    set_resolved_to_dummy()
                return
    
            li = xbmcgui.ListItem(list_item)
            if LIBRARY_FORMAT:    
                execute_video(filename, url, imdb_id, strm)
            else:
                execute_video(name, url, imdb_id, strm)
############################################### END STREAM FROM XBMC LIBRARY ##############################################################	

############################################### ONE CLICK STREAMING ##############################################################	
def one_click_movie(name, imdb_id, strm=False):
    open_playlists = True
    quality = CUSTOMQUALITY
    dialog = xbmcgui.Dialog()
    filename=name
    name2 = name[:len(data)-7].replace("The ","").lower()
    customstring="abcdef"
    menu_texts = []
	
    files = []
    operator="%7C"
    searchstring = "%s %s %s %s" % (str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ")), quality, operator, CUSTOMQUALITY2)
    files = search_furk(searchstring, "extended")
    count=0
    for f in files:
        if f.is_ready == "0":
            count=count+1
    if (count == len(files) and len(files)>0) or len(files)==0:
        time.sleep(F_DELAY)
        notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
        xbmc.executebuiltin(notify)
        files = search_furk(str(data.replace("-","").replace(" Documentary","").replace(" TV Movie","").replace(":","")), "all")
        count=0
        for f in files:
            if f.is_ready == "0":
                count=count+1

    if (count == len(files) and len(files)>0) or len(files)==0:
        menu_texts.append("...Search yify Movies HD")				
        menu_texts.append("...Search 1Channel")
        menu_texts.append("...Search Icefilms")
        menu_texts.append("...Search MovieStorm")
        menu_texts.append("...Search latest torrents")

        menu_id = dialog.select('No file found....try another addon?', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        if customstring!="abcdef":
            name=customstring
            name2=customstring
        if(menu_id == len(menu_texts)-5):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.yifymovies.hd'):
                name2 = name[:len(data)-7].replace("The ","")        
                xbmc.executebuiltin(('XBMC.Container.Update(%s?action=movies_search&query=%s)' %('plugin://plugin.video.yifymovies.hd/',urllib.quote_plus(name2))))
            else:
                dialog.ok("Addon not installed", "", "Install the yify Movies HD addon to use this function")
        elif(menu_id == len(menu_texts)-4):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
                xbmc.executebuiltin(('Container.Update(%s?mode=7000&section=&query=%s)' %('plugin://plugin.video.1channel/',name2)))
            else:
                dialog.ok("Addon not installed", "", "Install the 1Channel addon to use this function")
        elif(menu_id == len(menu_texts)-3):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
                url='http%3a%2f%2fwww.icefilms.info%2f'
                xbmc.executebuiltin(('Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',url,urllib.quote_plus(name2),"0")))
            else:
                dialog.ok("Addon not installed", "", "Install the IceFilms addon to use this function")
        elif(menu_id == len(menu_texts)-2):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.moviestorm'):
                url='http%3a%2f%2fwww.icefilms.info%2f'
                xbmc.executebuiltin(('Container.Update(%s?mode=7&url=%s&name=%s)' %('plugin://plugin.video.moviestorm/',"url",name2)))
            else:
                dialog.ok("Addon not installed", "", "Install the MovieStorm addon to use this function")
        elif(menu_id == len(menu_texts)-1):
            download_kat(str(data.replace("-"," ").replace(" Documentary","").replace(" TV Movie","").replace(":"," ")), "dummy")
    else:

        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Searching for files 1-Click')
        
        tracks = []
        count = 0
        for f in files:
            if f.type == "video" and f.url_dl != None:
                if FURK_LIM_FS:
                    if int(f.size)/1073741824 < FURK_LIM_FS_NUM:
                        if pDialog.iscanceled(): 
                            pDialog.close()
                            break
                        count = count + 1
                        if count > FURK_LIMIT:
                            pDialog.close()
                            break
                        percent = int(float(count * 100) / len(files))
                        text = "%s files found" % len(tracks)
                        pDialog.update(percent, text)
                        new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                        tracks.extend(new_tracks)
					
                else:
                    if pDialog.iscanceled(): 
                        pDialog.close()
                        break
                    count = count + 1
                    if count > FURK_LIMIT:
                        pDialog.close()
                        break
                    percent = int(float(count * 100) / len(files))
                    text = "%s files found" % len(tracks)
                    pDialog.update(percent, text)
                    new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                    tracks.extend(new_tracks)

        (url, name, id) = track_dialog(tracks)
        pDialog.close()
     
        if not url or not name:
            if strm:
                set_resolved_to_dummy()
            return
	
        if LIBRARY_FORMAT:    
            execute_video(filename, url, imdb_id, strm)
        else:
            execute_video(name, url, imdb_id, strm)
	
def one_click_episode(data, imdb_id, strm=False):
    open_playlists = True
    menu_texts = []
    menu_data = []
    menu_linkid = []
    menu_url_pls = []
    quality = TVCUSTOMQUALITY
    dialog = xbmcgui.Dialog()
    customstring="abcdef"
    menu_texts = []

    if re.search('<|>',data):
        data = data.split('<|>')
    else:
        if re.search('$',data):
            data = data.split('$')
    tv_show_name = data[0].replace(" Mini-Series","").replace("The ","")
    episode_name = data[1]
    season_number = int(data[2])
    episode_number = int(data[3])

    season_episode = "s%.2de%.2d" % (season_number, episode_number)
    season_episode2 = "%s %dx%.2d" % (tv_show_name, season_number, episode_number)
    season_episode3 = "%s season %d" % (tv_show_name, season_number)

    tv_show_season = "%s season" % (tv_show_name)
    tv_show_episode = "%s %s" % (tv_show_name, season_episode)
    track_filter = [episode_name, season_episode, season_episode2]
	
    files = []
    operator="%7C"
    searchstring = "%s %s %s %s" % (str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":","")), TVCUSTOMQUALITY, operator, TVCUSTOMQUALITY2)
    files = search_furk(searchstring, "extended")
    count=0
    for f in files:
        if f.is_ready == "0":
            count=count+1
    if (count == len(files) and len(files)>0) or len(files)==0:
        time.sleep(F_DELAY)
        notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
        xbmc.executebuiltin(notify)
        files = search_furk(str(tv_show_episode.replace("-"," ").replace(" Mini-Series","").replace(":","")), "all")
        count=0
        for f in files:
            if f.is_ready == "0":
                count=count+1

    if (count == len(files) and len(files)>0) or len(files)==0:
        menu_texts.append("...Search 1Channel")
        menu_texts.append("...Search Icefilms")
        menu_texts.append("...Search MovieStorm")
        menu_texts.append("...Search TVonline")
        menu_texts.append("...Search TV4ME")
        menu_texts.append("...Search latest torrents")

        menu_id = dialog.select('No file found....try another addon?', menu_texts)
        iname = "%s %sx%.2d" % (tv_show_name,season_number,episode_number)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        if customstring!="abcdef":
            easyname=customstring
            tv_show_name=customstring
            iname=customstring
        if(menu_id == len(menu_texts)-6):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
                xbmc.executebuiltin(('Container.Update(%s?mode=7000&section=tv&query=%s)' %('plugin://plugin.video.1channel/',tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the 1Channel addon to use this function")
        elif(menu_id == len(menu_texts)-5):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
                iurl='http%3a%2f%2fwww.icefilms.info%2f'
                xbmc.executebuiltin(('Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',iurl,urllib.quote(iname),"0")))
            else:
                dialog.ok("Addon not installed", "", "Install the Icefilms addon to use this function")
        elif(menu_id == len(menu_texts)-4):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.moviestorm'):
                xbmc.executebuiltin(('Container.Update(%s?mode=7&url=%s&name=%s)' %('plugin://plugin.video.moviestorm/',"url", tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the MovieStorm addon to use this function")
        elif(menu_id == len(menu_texts)-3):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.tvonline.cc'):
                xbmc.executebuiltin(('Container.Update(%s?mode=17&url=%s&name=%s)' %('plugin://plugin.video.tvonline.cc/',"url", tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the TVonline addon to use this function")
        elif(menu_id == len(menu_texts)-2):
            if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.tv4me'):
                xbmc.executebuiltin(('Container.Update(%s?mode=18&url=%s&name=%s)' %('plugin://plugin.video.tv4me/',"url", tv_show_name)))
            else:
                dialog.ok("Addon not installed", "", "Install the TV4ME addon to use this function")
        elif(menu_id == len(menu_texts)-1):
            download_kat(tv_show_name, season_episode)
    else:

        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Searching for files 1-Click')
        
        tracks = []
        count = 0
        for f in files:
            if f.type == "video" and f.url_dl != None:
                if FURK_LIM_FS_TV:
                    if int(f.size)/1073741824 < FURK_LIM_FS_NUM_TV:
                        if pDialog.iscanceled(): 
                            pDialog.close()
                            break
                        count = count + 1
                        if count > FURK_LIMIT:
                            pDialog.close()
                            break
                        percent = int(float(count * 100) / len(files))
                        text = "%s files found" % len(tracks)
                        pDialog.update(percent, text)
                        new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                        tracks.extend(new_tracks)
					
                else:
                    if pDialog.iscanceled(): 
                        pDialog.close()
                        break
                    count = count + 1
                    if count > FURK_LIMIT:
                        pDialog.close()
                        break
                    percent = int(float(count * 100) / len(files))
                    text = "%s files found" % len(tracks)
                    pDialog.update(percent, text)
                    new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                    tracks.extend(new_tracks)

        (url, name, id) = track_dialog(tracks)
        pDialog.close()
     
        if not url or not name:
            if strm:
                set_resolved_to_dummy()
            return
	
        li = xbmcgui.ListItem(clean_file_name(data))
        if LIBRARY_FORMAT:    
            execute_video(tv_show_episode, url, imdb_id, strm)
        else:
            execute_video(name, url, imdb_id, strm)

def get_playlist_tracks(playlist_file, open_playlists=False):######### SEARCH TRACKS #####
    tracks = []
    size = float(playlist_file.size)/1073741824
    id = playlist_file.id
 		
    try:
        if (name.endswith('.avi') or name.endswith('.mkv') or name.endswith('.mp4')) and name.lower().find("sample")<0 and name.lower().find("sampz")<0:
            tracks = [{'name': "[%.2fGB] " % size + name, 'location': playlist_file.url_dl, 'id': playlist_file.id}]#"[%.2fGB] " % size + 
        elif open_playlists:
            playlist_url = playlist_file.url_pls
            playlist = get_url(playlist_url)
            tracks = scrape_xspf(playlist, id)#, size, prefix
    except:
        pass
    return tracks
	
def scrape_xspf(body, id):############################# SCRAPE ARCHIVES #################
    all_track = regex_get_all(body, '<track>', '</track>')
    tracks = []
    for track in all_track:
        name = regex_from_to(track, '<title>', '</title>')
        location = regex_from_to(track, '<location>', '</location>')
        if (name.endswith('.mp4') or name.endswith('.avi') or name.endswith('.mkv')) and name.lower().find("sample")<0 and name.lower().find("sampz")<0:
            size = get_file_size(location)
            tracks.append({'name': "[%.2fGB] %s" % (size, name), 'location': location, 'id': id}) 
    return tracks
		
def track_dialog(tracks):################################# DRILL DOWN TO TRACKS ##########
    menu_texts = []
    menu_data = []
    menu_linkid = []
    for track in tracks:
        text = (track['name'])
        id = (track['id'])
        menu_texts.append(text)
        menu_data.append(track['location'])
        menu_linkid.append(track['id'])

    if len(menu_data) == 0:
        if mode != "wishlist search":
            builtin = 'XBMC.Notification(No files found,The search was unable to find any files,3000)'
            xbmc.executebuiltin(builtin)
        return (None, None)

    menu_id = 0
    if mode != "wishlist search":
        notify = 'XBMC.Notification(Starting stream,Be patient.......,5000)'
        xbmc.executebuiltin(notify)
		
    url = menu_data[menu_id]
    name = menu_texts[menu_id]
    id = menu_linkid[menu_id]
    
    return (url, name, id)
		
############################################### END ONE CLICK STREAMING ##############################################################	
def pc_setting():
    pw = ""
    dialog = xbmcgui.Dialog()
    keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password', True)
    keyboard.doModal()
    if keyboard.isConfirmed():
        pw = keyboard.getText()
        if pw == PC_PASS or pw == FURK_PASS:
            if PC_TOGGLE == "UNLOCKED":
                ADDON.setSetting('enable_pc_settings', value='LOCKED')
                xbmc.executebuiltin("Container.Refresh")
            else:
                ADDON.setSetting('enable_pc_settings', value='UNLOCKED')
                xbmc.executebuiltin("Container.Refresh")
                ADDON.openSettings()				
        else:
            dialog.ok("Incorrect PIN/Password","")			

def parental_control(imdb_id):
    dialog = xbmcgui.Dialog()
    rating_list = ["No thanks, I'll choose later", "Movies: G", "Movies: PG","Movies: PG-13", "Movies: R", "Movies: NC-17", "TV Shows: TV-Y/TV-Y7", "TV Shows: TV-Y7-FG", "TV Shows: TV-PG", "TV Shows: TV-14", "TV Shows: TV-MA"]
    rating_list_return = ["No thanks, I'll choose later", "G", "PG","PG-13", "R", "NC-17", "TV-Y", "TV-Y7-FG", "TV-PG", "TV-14", "TV-MA"]
    if imdb_id=="":
        mpaa = PC_DEFAULT
    data_file =  os.path.join(META_PATH, "%s%s" % (imdb_id,".dat"))
    if not(os.path.isfile(data_file)) and imdb_id != "":
        rating_id = dialog.select("No rating found....set/save your own?", rating_list)
        rating = rating_list_return[rating_id]
        if(rating_id <= 0):
            return (None, None)
            dialog.close()
        
        content = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % ("", "", "", "", "", "", "", "", "", rating)
        write_to_file(data_file, content)
			
    if os.path.isfile(data_file):
        content = read_from_file(data_file)
        data = content.split('\n')
        if len(data) == 10:
            mpaa = data[9]
            if mpaa == "":
                title = data[0]
                year = data[1]
                genre = data[2]
                tagline = data[3]
                overview = data[4]
                duration = data[5]
                rating = data[6]
                votes = data[7]
                premiered = data[8]
                rating_id = dialog.select("No rating found....set/save your own?", rating_list)
                if(rating_id <= 0):
                    return (None, None)
                    dialog.close()
                pw=''
                keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password to save the rating', True)
                keyboard.doModal()
                if keyboard.isConfirmed():
                    pw = keyboard.getText()
                else:
                    pw=''
                if pw == PC_PASS or pw == FURK_PASS:
                    mpaa = rating_list_return[rating_id]
                    content = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (title, year, genre, tagline, overview, duration, rating, votes, premiered, mpaa)
                    write_to_file(data_file, content)
                else:
                    mpaa = PC_DEFAULT
 
        else:
            mpaa = data[7]
            if mpaa == "":
                title = data[0]
                year = data[1]
                genre = data[2]
                overview = data[3]
                rating = data[4]
                votes = data[5]
                premiered = data[6]
                rating_id = dialog.select("No rating found....set/save your own?", rating_list)
                if(rating_id <= 0):
                    return (None, None)
                    dialog.close()
                pw=''
                keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password to save the rating', True)
                keyboard.doModal()
                if keyboard.isConfirmed():
                    pw = keyboard.getText()
                else:
                    pw=''
                if pw == PC_PASS or pw == FURK_PASS:
                    mpaa = rating_list_return[rating_id]
                    content = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (title, year, genre, overview, rating, votes, premiered, mpaa)
                    write_to_file(data_file, content)
                else:
                    mpaa = PC_DEFAULT
    else:
        if PC_DEFAULT == "PLAY":
            mpaa = "PLAY"
        else:
            mpaa = "REQUIRE PIN"
    if mpaa == "PLAY":
        mpaa = 0
    elif mpaa == "TV-Y" or mpaa == "TV-Y7" or mpaa == "TV-G" or mpaa == "G":
        mpaa = 1
    elif mpaa == "TV-Y7-FG" or mpaa == "TV-PG" or mpaa == "PG":
        mpaa = 2
    elif mpaa == "TV-14" or mpaa == "PG-13":
        mpaa = 3
    elif mpaa == "TV-MA" or mpaa == "R" or mpaa == "NC-17" or mpaa == "REQUIRE PIN":
        mpaa = 4
    return mpaa
	

def execute_video(name, url, list_item, strm=False):
    now = time.strftime("%H")
    dialog = xbmcgui.Dialog()
    if list_item.find('$')>0:
        imdb_id = list_item.split('$')[2]
    else:
        imdb_id=list_item
    if PC_ENABLE:
        mpaa = parental_control(imdb_id)
    else:
        mpaa = 0
    pw=''
    if mpaa >= PC_RATING and PC_ENABLE and ((int(now) < int(PC_WATERSHED) and int(now) > 6) or int(PC_WATERSHED) == 25):
        keyboard = xbmc.Keyboard(pw, 'Enter your PIN/Password to play', True)
        keyboard.doModal()
        if keyboard.isConfirmed():
            pw = keyboard.getText()
        else:
            pw=''
    if int(now) >= int(PC_WATERSHED) or not(PC_ENABLE) or ((pw == PC_PASS or pw == FURK_PASS) or mpaa < PC_RATING or (int(now) < 6 and int(PC_WATERSHED) != 25)):
        poster_path = create_directory(META_PATH, META_QUALITY)
        poster_file = os.path.join(poster_path, "%s_poster.jpg" % (imdb_id))
        list_item = xbmcgui.ListItem(clean_file_name(name, use_blanks=False), iconImage=poster_file, thumbnailImage=poster_file)
        
        list_item.setThumbnailImage(poster_file)
        if PLAY_MODE == 'stream':
            if mode == "strm file dialog" or strm:
                set_resolved_url(int(sys.argv[1]), name, url, imdb_id) 
            else:
                play(name, url, list_item)
        elif PLAY_MODE == 'download and play':
            if strm:
                download_and_play(name, url, play=True, handle=int(sys.argv[1]))
            else:
                download_and_play(name, url, play=True)
    else:
        dialog.ok("You cannot play this video","PIN incorrect")
    
			
############################################### CONTEXT MENU FUNCTIONS ##############################################################	
def add_download(name, info_hash):
    dialog = xbmcgui.Dialog()
    if mode == "wishlist search":
        FURK.dl_add(info_hash)
    else:
        if dialog.yesno("Add Download", "Download this file to your Furk account?", "Success depends on number of seeders"):
            response = FURK.dl_add(info_hash)
            if response['status'] == 'ok':
                notify = 'XBMC.Notification(Download added to Furk account,Check status in My Files,3000)'
                xbmc.executebuiltin(notify)
            else:
                notify = 'XBMC.Notification(Error,Unable to add download,3000)'
                xbmc.executebuiltin(notify)
			
def add_wishlist(name, type):
    name = name.replace("(","").replace(")","")
    dialog = xbmcgui.Dialog()
    quality_list = ["Custom","Any", "1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
    quality_list_return = ["custom", "any","1080P", "720P", "DVDSCR", "SCREENER", "BDRIP", "BRRIP", "BluRay 720P", "BluRay 1080P", "DVDRIP", "R5", "HDTV", "TELESYNC", "TS", "CAM"]
    quality_id = dialog.select("Select your preferred quality", quality_list)
    if(quality_id == 0):
        quality = name
        keyboard = xbmc.Keyboard(quality, 'Custom Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            quality = keyboard.getText()
    else:
        quality = quality_list_return[quality_id]
    if(quality_id < 0):
        return (None, None)
        dialog.close()
		
    action_list = ["Download","Add Stream", "Add to My Files", "Check for new torrents"]
    action_list_return = ["download","stream", "myfiles", "newtorrents"]
    action_id = dialog.select("What would you like to do?", action_list)
    action = action_list_return[action_id]
    if(action_id < 0):
        return (None, None)
        dialog.close()
    episode = type
    list_data = "%s %s<|>%s<|>%s" % (name, quality, action, episode)
    add_search_query(list_data, WISHLIST)
	
def add_people(name, data, imdb_id):
    list_data = "%s<|>%s<|>%s" % (name, data, imdb_id)
    add_search_query(list_data, PEOPLE_LIST)

def view_trailer(name, imdb_id, xbmcname, strm=False):
    menu_texts = []
    menu_data = []
    menu_res = []
    menu_list_item = []
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Searching for trailer')
    dialog = xbmcgui.Dialog()
    try:
        url = "http://www.hd-trailers.net/movie/" + name
        response = get_url(url, cache=CACHE_PATH)
        match=re.compile('href="http://(.+?)" rel=(.+?)title="(.+?)">(.+?)</a></td>').findall(response) 
        if len(match)==0:
            url = "http://www.hd-trailers.net/movie/" + name.replace('and','')
            response = get_url(url, cache=CACHE_PATH)
            match=re.compile('href="http://(.+?)" rel=(.+?)title="(.+?)">(.+?)</a></td>').findall(response) 
            if len(match)==0:
                dialog.ok("Trailer Search", 'No trailers found for:', xbmcname) 
                return
        for url, info, title, res in match:
            if url.find('apple')>0:
                url = '%s|User-Agent=QuickTime' % ("http://" + url)
            elif url.find('youtube')>0:
                video_id = url.replace('www.youtube.com/watch?v=','')
                url = (
                    'plugin://plugin.video.youtube/'
                    '?action=play_video&videoid=%s' % video_id
                )
            else:
                url = "http://" + url
            if TRAILER_RESTRICT:
                if url.find('yahoo')<0 and res==TRAILER_QUALITY:
                    menu_texts.append("[%s] %s" % (res, clean_file_name(title, use_blanks=False)))
                    menu_list_item.append(clean_file_name(title, use_blanks=False))
                    menu_data.append(url)
                    menu_res.append(res)
            else:
                if url.find('yahoo')<0:
                    menu_texts.append("[%s] %s" % (res, clean_file_name(title, use_blanks=False)))
                    menu_list_item.append(clean_file_name(title, use_blanks=False))
                    menu_data.append(url)
                    menu_res.append(res)
					
        if TRAILER_ONECLICK:
            menu_id =0
        else:
            menu_id = dialog.select('Select Trailer', menu_texts)
        if(menu_id < 0):
            return (None, None)
            dialog.close()
        else:	
            url = menu_data[menu_id]
            name = menu_texts[menu_id]
            list_item = menu_list_item[menu_id]
			
        pDialog.close()
    
        if not url or not name:
            if strm:
                set_resolved_to_dummy()
            return
    
        li = xbmcgui.ListItem(list_item)
    
        execute_video(name, url, imdb_id, strm)
    except:
        dialog.ok("Trailer Search", 'No trailers found for:', xbmcname)
		
def myfiles_add(name, id):
    dialog = xbmcgui.Dialog()
    response = FURK.file_link(id)

    if response['status'] == 'ok':
        dialog.ok("Add to My Files", name, 'Success - Added to My Files')
    else:
        dialog.ok("Add to My Files", name, response['status']) 
    return (None, None)
    dialog.close()

def myfiles_remove(name, id):
    dialog = xbmcgui.Dialog()
    response = FURK.file_unlink(id)
    if response['status'] == 'ok':
        dialog.ok("Remove from My Files", name, 'Success')
    else:
        dialog.ok("Remove from My Files", name, 'Error')
    return (None, None)
    dialog.close()
	
def myfiles_clear(name, id):
    dialog = xbmcgui.Dialog()
    response = FURK.file_clear(id)

    if response['status'] == 'ok':
        dialog.ok("Clear Deleted file", name, 'Success - File removed')
    else:
        dialog.ok("Clear Deleted file", name, response['status']) 
    return (None, None)
    dialog.close()


def myfiles_protect(name, id):
    dialog = xbmcgui.Dialog()
    is_protected = '1'
    response = FURK.file_protect(id, is_protected)
    if response['status'] == 'ok':
        dialog.ok("File Protection", name, 'Protected')
    else:
        if response['error'] == 'limit exceeded':
            dialog.ok("File Protection", name, 'Error! Your storage limit for protected files is exceeded','Current usage is ' + response['usage'] + ' GB')
        elif response['error'] == 'not premium':
            dialog.ok("File Protection", name, 'Error! This feature is for premium users only')
        elif response['status'] == 'error':
            dialog.ok("File Protection", name, response['error'])
    return (None, None)
    dialog.close()


def myfiles_unprotect(name, id):
    dialog = xbmcgui.Dialog()
    is_protected = '0'
    response = FURK.file_protect(id, is_protected)
    if response['status'] == 'ok':
        dialog.ok("File Protection", name, 'Unprotected')
    else:
        if response['error'] == 'limit exceeded':
            dialog.ok("File Protection", name, 'Error! Your storage limit for protected files is exceeded','Current usage is ' + response['usage'] + ' GB')
        elif response['error'] == 'not premium':
            dialog.ok("File Protection", name, 'Error! This feature is for premium users only')
        elif response['status'] == 'error':
            dialog.ok("File Protection", name, response['error'])
    return (None, None)
    dialog.close()	

############################################### END CONTEXT MENU FUNCTIONS ##############################################################
	
def one_click_download():
    open_playlists = True
    sleep = 10
    if os.path.isfile(WISHLIST):
        s = read_from_file(WISHLIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<|>')
                action = list[1]
                episode = list[2]
                if episode == "dummy":
                    searchname1 = list[0]
                else:
                    searchname1 = "%s %s" % (list[0], list[2])
                searchname = searchname1.replace(" any","")
	
                if action == "newtorrents":
                    name = list[0]
                    download_kat(name, episode)
                else:	
                    files = []
                    files = search_furk(str(searchname), "all")
                    if len(files)==0:
                        if mode != "wishlist search":
                            notify = 'XBMC.Notification(No custom-quality files found,Now searching for any quality,3000)'
                            xbmc.executebuiltin(notify)
                    else:        
                        tracks = []
                        count = 0
                        for f in files:
                            if f.type == "video" and f.url_dl != None:
                                if FURK_LIM_FS:
                                    if int(f.size)/1073741824 < FURK_LIM_FS_NUM:
                                        new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                                        tracks.extend(new_tracks)
					
                                else:
                                    new_tracks = get_playlist_tracks(f, open_playlists=open_playlists)
                                    tracks.extend(new_tracks)
                        try:
                            (url, name, id) = track_dialog(tracks)
                            if LIBRARY_FORMAT:
                                name = "%s.%s" % (str(searchname.lower()),name.lower()[len(name)-3:])
                            else:
                                name = name.lower()
                            if action == "download":
                                if episode == "dummy":
                                    type = "movie"
                                else:
                                    type = "tv"
                                download_only(name, url, type)
                            if action == "stream":
                                if episode == "dummy":
                                    path = MOVIES_PATH
                                else:
                                    path = TV_SHOWS_PATH
                                create_strm_file(name, url, id, "strm file dialog", path)
                            if action == "myfiles":
                                FURK.file_link(id)
                            name = list[0]
                            list_data = "%s<|>%s<|>%s" % (name, action, episode)
                            remove_search_query(list_data, WISHLIST)
                            add_search_query(list_data, WISHLIST_FINISHED)
                        except:
                            pass

                    sleep = sleep + 1				
                    time.sleep(sleep) #sleep for 10+ seconds to get around furk api call limit. 
                    print "What the Furk......sleeping for " + str(sleep) + " seconds"
        scan_library() # scan library when finished
            
def set_resolved_to_dummy():
    listitem = xbmcgui.ListItem('Dummy data to avoid error message', path=DUMMY_PATH)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


def search_furk(query, match, sort=FURK_SORT+',size', filter=FURK_RESULTS, moderated=FURK_MODERATED):
    query = clean_file_name(query)
    query = query.replace('\'', ' ')
    if not login_at_furk():
        return []
    
    files = []
    if type(query).__name__ == 'list':
        for q in query:
            search_result = FURK.search(q, match, sort=FURK_SORT+',size', filter=FURK_RESULTS, moderated=FURK_MODERATED)
            if search_result.query_changed == None:
                files.extend(search_result.files)
    else:
        search_result = FURK.search(query, match, sort=FURK_SORT+',size', filter=FURK_RESULTS, moderated=FURK_MODERATED)
        if search_result.query_changed == None:
            files = search_result.files
    return files
	
###################################################################	
def myfiles(unlinked, strm=False):
    items = []
	
    if not login_at_furk():
        return []
		
    files = []
    my_files = FURK.file_get(unlinked)
    files = my_files.files
	
    for f in files:
        count_files = (f.files_num_video)
        name = f.name
        url = f.url_dl
        id = f.id
        size = f.size
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        text = "%s %s [%s files]" %(size, name, count_files)
        try:
            poster = f.ss_urls_tn[0]
        except:
            poster = ""
        xbmcname = name

        mode = "t files menu"
        try:
            archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, "",  "movie")
            items.append(archive_tuple)
            setView('movies', 'movies-view')
        except:
            pass
    return items;


def get_downloads(dl_status):
    downloads = str(FURK.dl_get(dl_status))
    dls_all = regex_from_to(str(downloads), "dls': ", ", u'found_dls")
    all_dls = regex_get_all(dls_all, '{', 'None}')
    
    items = []
    for dls in all_dls:
        name = regex_from_to(dls, "name': u'", "', u")
        size = regex_from_to(dls, "size': u'", "', u")
        speed = regex_from_to(dls, "speed': u'", "', u")
        downloaded = regex_from_to(dls, "have': u'", "', u")
        seeders = regex_from_to(dls, "seeders': u'", "', u")
        id = regex_from_to(dls, "id': u'", "', u")
        fail_reason = regex_from_to(dls, "fail_reason': u'", "', u")
        size = float(size)/1073741824
        size = "[%.2fGB]" % size
        if int(speed) < 1048576:
            speed = float(speed)/1024
            speed = "[%.0fkB/s]" % speed
        else:
            speed = float(speed)/1024/1024
            speed = "[%.0fMB/s]" % speed
        downloaded = downloaded + "%"
		
        mode = "delete dls"
        archive_tuple = create_dls_tuple(name, size, speed, mode, downloaded, str(id), seeders, fail_reason)
        items.append(archive_tuple)

    return items;


######################################################################
def display_error(text1, text2):
    dialog = xbmcgui.Dialog()
    dialog.ok("Houston we have a problem",text1, text2, "Visit www.xbmchub.com/forums/what-furk/ for help")
	
################# MUSIC ########################################################################################
def search_artist():
    if mode == 'search artist menu':
        keyboard = xbmc.Keyboard('', 'Search Artist', False)
    else:
        keyboard = xbmc.Keyboard('', 'Search Album', False)
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_artists(query)

def search_artists(query):
    music=[]
    if mode == 'search artist menu':
        artist=query.replace(' ', '+')  
        link = get_url('http://www.allmusic.com/search/artists/'+artist)
        match=re.compile('<div class="photo">\n.+?a href="(.+?)" data-tooltip=".+?">\n.+?img src="(.+?).jpg.+?" height=".+?" alt="(.+?)">').findall(link)
        for url,icon,artist in match:
            url='http://www.allmusic.com'+url+'/discography'
            iconimage=icon.replace('JPG_170','JPG_400')+'.jpg'
            addDir(clean_file_name(artist),url,'discography menu',iconimage)
    else:
        album=query.replace(' ', '+') 
        link = get_url('http://www.allmusic.com/search/albums/'+album).replace('\n','')
        match=re.compile('<div class="cover">.+?href="(.+?)" title="(.+?)".+?<img src="(.+?).jpg.+?".+?<div class="artist">.+?a href=".+?">(.+?)</a>').findall(link)
        for url,name,icon,artist in match:
            url='http://www.allmusic.com'+'/album'+url
            iconimage=icon.replace('JPG_170','JPG_250')+'.jpg'
            addDir(artist, name,'music file disc menu',iconimage)

def discography(artist,url,icon):
    music=[]
    link = get_url(url)
    match=re.compile('<td class="cover">\n.+?a href="(.+?)"\n.+?title="(.+?)"\n.+?data-tooltip=".+?">\n.+?div class=".+?" style=".+?" ><img class=".+?" src=".+?" data-original="(.+?).jpg.+?"').findall(link)
    uniques=[]
    addDir(artist, "Discography",'music file disc menu',icon)
    for url,name,iconimage in match:
        if name not in uniques:
            uniques.append(name)
            url='http://www.allmusic.com'+'/album'+url
            iconimage=iconimage.replace('JPG_250','JPG_400').replace('JPG_75','JPG_400')+'.jpg'
            name=str(name).replace("'",'').replace(',','') .replace(":",'').replace('&amp;','And').replace('.','')
            addDir(artist, name,'music file disc menu',iconimage)
			
def music_lists(url):
    music = []
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    if mode == "ukofficial menu":
        all_list = regex_get_all(link, '<div class="previewwindow">', '</div>')
        for list in all_list:
            icon = regex_from_to(list, 'src="', '" />')
            title = clean_file_name(regex_from_to(list, '<h3>', '</h3>')).replace('&#039;',"'")
            name = clean_file_name(regex_from_to(list, '<h4>', '</h4>')).replace('&#039;',"'")
            music.append({'name': name, 'title': title, 'icon': icon})
    elif mode == "billboard menu":
        match = re.compile('"title" : "(.+?)"\r\n.+?"artist" : "(.+?)"\r\n.+?image" : "(.+?)"\r\n.+?"entityId" : ".+?"\r\n.+?"entityUrl" : "(.+?)"').findall(link)
        for name, artist, iconimage, url in match:
            artist=artist.replace('&','And')
            url='http://www1.billboard.com'+url+'#'+url
            if re.search('.gif',iconimage):
                iconimage=""
            music.append({'name': artist, 'title': name, 'icon': iconimage})
      
    return create_music_items(music)
	
def music_dialog(name, data, imdb_id):
    items = []
    icon=imdb_id
    name1 = name
    name2 = "%s %s" % (name, data)
    if FURK_SEARCH_MF:
        try:
            mfiles = []
            my_files = FURK.file_get('0')
            mfiles = my_files.files
            name3 = name.lower()
            for f in mfiles:
                if name3.replace(' &', '').replace(' and', '') in f.name.lower():
                    name = clean_file_name(f.name)
                    url = f.url_dl
                    id = f.id
                    size = f.size
                    size = float(size)/1073741824
                    size = "[%.2fGB]" % size
                    text = '[COLOR gold]' + "%s %s %s" %("MF:",size, clean_file_name(f.name)) + '[/COLOR]'
                    xbmcname = str("%s | %s" % (name1, data))

                    mode = "t music files menu"
                    archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, "", "",  "movie")
                    items.append(archive_tuple)
        except:
            pass
        time.sleep(F_DELAY)
		
    files = []

    searchstring = name2
    files = search_furk(searchstring, "all")
    dialog = xbmcgui.Dialog()
    if len(files) == 0:
        dialog.ok("File Search", 'No files found for: ' + searchstring)
        return (None, None)

    for f in files:
        if f.type != "video":
            name = f.name.encode('utf-8','ignore')
            url = f.url_dl
            id = f.id
            is_ready = f.is_ready
            info_hash = f.info_hash
            size = f.size
            size = float(size)/1073741824
            size = "[%.2fGB]" % size
            text = "%s %s" %(size, name)
            poster=icon
            xbmcname = str("%s | %s" % (name1, data))
            if  is_ready == "1" and f.url_dl != None:
                text = '[COLOR cyan]' + "%s %s" %(size, clean_file_name(name)) + '[/COLOR]'
                mode = "t music files menu"
            else:
                text = '[COLOR red]' + "%s %s" %(size, clean_file_name(name))+ '[/COLOR]'
                poster = ""
                id = info_hash
                mode = "add download"

            archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, imdb_id, "movie")
            items.append(archive_tuple)
	
    return items;
	
def t_file_dialog_music(xbmcname, id, imdb_id, clear):################### EXPLORE T FILES ##########################################
    items = []
    files = []
    browse=False
    thumb=imdb_id
    try:
        namesplit=xbmcname.split(' | ')
        artist=namesplit[0]
        album=namesplit[1]
    except:
        pass

    dialog = xbmcgui.Dialog()
    my_files = FURK.t_file_get(id, t_files="1")
    files = my_files.files
    for f in files:
        t_files = f.t_files
    all_tf = regex_get_all(str(t_files), "{", "'}")
    nItem = len(all_tf)
    playlist=[]
    if mode != "t music queue menu":
        if dialog.yesno("WTF Music", 'Browse songs or play full album?', '', '', 'Play Now','Browse'):
            browse=True
    if browse==True:	
        for tf in all_tf:
            all_td = regex_get_all(tf, "{", "'}")
            name = regex_from_to(str(all_td), "name': u'", "', u")
            if name[len(name)-3:] == 'lac':
                format = 'flac'
            else:
                format = name[len(name)-3:]
            url = regex_from_to(str(all_td), "url_dl': u'", "', u")
            size = regex_from_to(str(all_td), "size': u'", "'")
            size = float(size)/1048576
            size = "[%.1fMB]" % size
            text = "[%s] %s %s" %(format, size, clean_file_name(name))

            pl = get_XBMCPlaylist(clear=False)
            if name[len(name)-3:] == 'lac' or name[len(name)-3:] == 'mp3' or name[len(name)-3:] == 'wma':
                addLink(clean_file_name(name),url,thumb, xbmcname)
                liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
                try:
                    liz.setInfo('music', {'Artist':artist, 'Album':album})
                except:
                    liz.setInfo('music', {'Artist':clean_file_name(xbmcname), 'Album':''})
                liz.setProperty('mimetype', 'audio/mpeg')
                liz.setProperty('fanart_image', fanart)
                liz.setThumbnailImage(thumb)
                playlist.append((url, liz))
                
    else:
        for tf in all_tf:
            all_td = regex_get_all(tf, "{", "'}")
            name = regex_from_to(str(all_td), "name': u'", "', u")
            if name[len(name)-3:] == 'lac':
                format = 'flac'
            else:
                format = name[len(name)-3:]
            url = regex_from_to(str(all_td), "url_dl': u'", "', u")
            size = regex_from_to(str(all_td), "size': u'", "'")
            size = float(size)/1048576
            size = "[%.1fMB]" % size
            text = "[%s] %s %s" %(format, size, clean_file_name(name))
            dp = xbmcgui.DialogProgress()
            dp.create("Pearl Jam Live",'Creating Your Playlist')
            dp.update(0)
            pl = get_XBMCPlaylist(clear)
            if name[len(name)-3:] == 'lac' or name[len(name)-3:] == 'mp3' or name[len(name)-3:] == 'wma':
                addLink(clean_file_name(name),url,thumb, xbmcname)
                liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
                try:
                    liz.setInfo('music', {'Artist':artist, 'Album':album})
                except:
                    liz.setInfo('music', {'Artist':clean_file_name(xbmcname), 'Album':''})
                liz.setProperty('mimetype', 'audio/mpeg')
                liz.setThumbnailImage(thumb)
                liz.setProperty('fanart_image', fanart)
                if format != "flac":
                    playlist.append((url, liz))

                progress = len(playlist) / float(nItem) * 100               
                dp.update(int(progress), 'Adding to Your Playlist',name)
                if dp.iscanceled():
                    return

        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
        if clear or (not xbmc.Player().isPlayingAudio()):
            xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(pl)
			
def add_audio_stream(xbmcname, id, imdb_id):
    items = []
    files = []
    if xbmcname.find(' | ')>0:
        namesplit=xbmcname.split(' | ')
        artist=namesplit[0]
        album=namesplit[1]
    else:
        artist="My Files Downloads"
        album=xbmcname
    notify = "%s,%s,%s" % ('XBMC.Notification(Adding stream files to your Music folder',xbmcname,'2000)')
    xbmc.executebuiltin(notify)
    artist_path = create_directory(DOWNLOAD_MUS, clean_file_name(artist, use_blanks=False))
    album_path = create_directory(artist_path, clean_file_name(album, use_blanks=False))

    my_files = FURK.t_file_get(id, t_files="1")
    files = my_files.files
    for f in files:
        t_files = f.t_files
    all_tf = regex_get_all(str(t_files), "{", "'}")

    for tf in all_tf:
        all_td = regex_get_all(tf, "{", "'}")
        name = regex_from_to(str(all_td), "name': u'", "', u")
        url = regex_from_to(str(all_td), "url_dl': u'", "', u")
        text = clean_file_name(name)
        if name[len(name)-3:] != "jpg" and name[len(name)-3:] != "txt" and name[len(name)-3:] != "nfo":
            strm_string = str(url)
            filename = clean_file_name("%s.strm" % name[:-4])
            path = os.path.join(album_path, filename)
            stream_file = open(path, 'w')
            stream_file.write(strm_string)
            stream_file.close()
		
    notify = "%s,%s,%s" % ('XBMC.Notification(Finished Adding Streams',xbmcname,'4000)')
    xbmc.executebuiltin(notify)

	
def get_XBMCPlaylist(clear):
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    if clear:
        pl.clear()
    return pl

    dialog = xbmcgui.Dialog()
    if dialog.yesno("Pearl Jam Live", 'Queue album or play now?', '', '', 'Play Now','Queue') == 0:
        pl.clear()
    return pl
	
def myfiles_audio(unlinked):
    items = []
	
    if not login_at_furk():
        return []
		
    files = []
    my_files = FURK.file_get(unlinked)
    files = my_files.files
	
    for f in files:
        if f.type != "video":
            name = f.name
            url = f.url_dl
            id = f.id
            size = f.size
            size = float(size)/1048576
            size = "[%.1fMB]" % size
            text = "%s %s" %(size, clean_file_name(name))
            poster = ''
            xbmcname = name

            mode = "t music files menu"
            try:
                archive_tuple = create_archive_tuple(xbmcname, text, name, mode, url, str(id), size, poster, "","")
                items.append(archive_tuple)
                setView('movies', 'movies-view')
            except:
                pass
    return items;
	

	
def addLink(name,url,iconimage,albumname):
    contextMenuItems = []
    ok=True
    download_url = '%s?name=%s&data=%s&imdb_id=%s&mode=download song' % (sys.argv[0], urllib.quote(albumname), url, name)  
    contextMenuItems.append(('Download Song', 'XBMC.RunPlugin(%s)' % download_url))
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    liz.setInfo( type="Audio", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name,data,mode,imdb_id,infoLabels=None):
    contextMenuItems = []
    u=sys.argv[0]+"?data="+urllib.quote_plus(data)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&imdb_id="+str(imdb_id)
    ok=True
    if mode =="music file disc menu":
        liz=xbmcgui.ListItem("%s | %s" % (name, '[COLOR gold]' + data + '[/COLOR]'), iconImage="DefaultFolder.png", thumbnailImage=imdb_id)
    else:
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=imdb_id)
    contextMenuItems.append(('Search for music videos', "XBMC.Container.Update(%s?mode=music video menu&name=%s&data=%s&imdb_id=%s)" % (sys.argv[0], urllib.quote(name), "", "" ) ) )
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    if mode =="music file disc menu":
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
    else:
        liz.setInfo( type="Video", infoLabels=infoLabels)
        try:
            liz.setProperty( "fanart_image", infoLabels['fanart'] )
        except:
            liz.setProperty('fanart_image', fanart )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
	
def addDir2(name,data,mode,imdb_id):
    u=sys.argv[0]+"?data="+urllib.quote_plus(data)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&imdb_id="+str(imdb_id)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=imdb_id)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
	
def addDir3(name,data,mode,imdb_id):
    u=sys.argv[0]+"?data="+urllib.quote_plus(data)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&imdb_id="+str(imdb_id)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=imdb_id)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

################# END MUSIC ####################################################################################

def create_movie_items(movies, start, pname):
    items = []
    missing_meta = []
    addDir2('[COLOR cyan]' + "<<< Return to Movies" + '[/COLOR]',"","imdb menu","")
    for movie in movies:
        if movie['year'] == "rem":
            name = movie['name']
        else:
		    name = "%s (%s)" % (movie['name'], movie['year'])

        imdb_id = movie['imdb_id']
        try:
            rating = movie['rating']
            votes = movie['votes']
        except:
            rating = '0'
            votes = '0'

        movie_tuple = create_movie_tuple(name, imdb_id, rating, votes)
        items.append(movie_tuple)

        if (not meta_exist(imdb_id, META_PATH) or imdb_id==None) and votes!="NP" and votes!="JP":
            missing_meta.append(imdb_id)
	
    return items, missing_meta


def create_tv_show_items(tv_shows, start, pname):
    items = []
    missing_meta = []
    addDir2('[COLOR cyan]' + "<<< Return to Movies" + '[/COLOR]',"","imdb menu","")

    for tv_show in tv_shows:
        if tv_show['year'] == "rem":
            name = tv_show['name']
        else:
            name = "%s (%s)" % (tv_show['name'], tv_show['year'])
        imdb_id = tv_show['imdb_id']
        try:
            rating = tv_show['rating']
            votes = tv_show['votes']
        except:
            rating = '0'
            votes = '0'
        tv_show_tuple = create_tv_show_tuple(name, imdb_id, rating, votes)
        items.append(tv_show_tuple)
        if (not meta_exist(imdb_id, META_PATH) or imdb_id==None) and votes!="NP":
            missing_meta.append(imdb_id)

    
    return items, missing_meta
	
def create_actor_items(actors):
    items = []

    for actor in actors:
        name = actor['name']
        photo = actor['photo']
        imdb_id = actor['imdb_id']
        profession = actor['profession']
        actor_tuple = create_actor_tuple(name, photo, imdb_id, profession)
        items.append(actor_tuple)
    
    return items
	
def create_music_items(music):
    items = []

    for m in music:
        name = m['name']
        title = m['title']
        icon = m['icon']
        music_tuple = create_music_tuple(name, title, icon)
        items.append(music_tuple)
    
    return items
	
def create_music_tuple(name, title, icon):
    music_url = create_url(name, "music file menu", title, icon)
    music_list_item = create_music_list_item(name, icon, title);
    music_tuple = (music_url, music_list_item, True)
    return music_tuple
	
def create_music_list_item(name, icon, title):
    contextMenuItems = []
    text = "%s | %s" % (name, '[COLOR gold]' + title + '[/COLOR]')
    contextMenuItems.append(('Search for music videos', "XBMC.Container.Update(%s?mode=music video menu&name=%s&data=%s&imdb_id=%s)" % (sys.argv[0], urllib.quote(name), "", "" ) ) )
    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setIconImage(icon)
    return li

def create_actor_tuple(name, photo, imdb_id, profession):
    actor_url = create_url(name, "actor movies menu", imdb_id, "")
    actor_list_item = create_actor_list_item(name, photo, imdb_id, profession);
    actor_tuple = (actor_url, actor_list_item, True)
    return actor_tuple

def create_movie_tuple(name, imdb_id, rating, votes):
    if votes == 'NP':
        start=str(int(rating)+IMDB_RESULTS)
        movie_url = create_url(name, mode, start, imdb_id)
    elif votes == 'NW':
        start=str(int(rating)+250)
        movie_url = create_url(name, mode, start, imdb_id)
    elif votes == 'D':
        movie_url = create_url(name.replace('IMDB USERS WHO LIKE ','').replace(' ALSO LIKE:',''), "movie result menu", "", imdb_id)
    else:
        movie_url = create_url(name, "movie result menu", "", imdb_id)
    movie_list_item = create_movie_list_item(name, imdb_id, rating, votes);
    movie_tuple = (movie_url, movie_list_item, True)
    return movie_tuple

def create_movie_directory_tuple(name, mode, start):
    movie_directory_url = create_url("", mode, start, name)
    movie_directory_list_item = create_movie_directory_list_item(name, mode);
    movie_directory_tuple = (movie_directory_url, movie_directory_list_item, True)
    return movie_directory_tuple

def create_directory_tuple(name, mode):
    directory_url = create_url(name, mode, data, "")
    directory_list_item = create_directory_list_item(name, mode);
    directory_tuple = (directory_url, directory_list_item, True)
    return directory_tuple
    return directory_tuple
	
def create_subdirectory_tuple(name, mode, data):
    subdirectory_url = create_url(name, mode, data, "")
    subdirectory_list_item = create_sub_directory_list_item(name, mode);
    subdirectory_tuple = (subdirectory_url, subdirectory_list_item, True)
    return subdirectory_tuple

def create_tv_show_tuple(name, imdb_id, rating, votes):
    if votes == 'NP':
        start=str(int(rating)+IMDB_RESULTS)
        tv_show_url = create_url(name, mode, start, imdb_id)
    else:
        tv_show_url = create_url(name.replace('IMDB USERS WHO LIKE ','').replace(' ALSO LIKE:',''), "seasons menu", "", imdb_id)
    tv_show_list_item = create_tv_show_list_item(name, imdb_id, rating, votes);
    tv_show_tuple = (tv_show_url, tv_show_list_item, True)
    return tv_show_tuple

def create_season_tuple(name, data, imdb_id, poster, fanart):
    season_url = create_url(name, 'episodes menu', data, imdb_id)
    season_list_item = create_season_list_item(name, data, imdb_id, poster, fanart);
    season_tuple = (season_url, season_list_item, True)
    return season_tuple

def create_episode_tuple(name, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname):
    episode_url = create_url(name, "episode result menu", data, imdb_id)
    episode_list_item = create_episode_list_item(name, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname);
    episode_tuple = (episode_url, episode_list_item, True)
    return episode_tuple
	
def create_furk_search_tuple(query):
    furk_search_url = create_url(query, 'furk result dialog menu', query, "")
    furk_search_list_item = create_furk_search_list_item(query);
    furk_search_tuple = (furk_search_url, furk_search_list_item, True)
    return furk_search_tuple

def create_imdb_search_tuple(query):
    imdb_search_url = create_url(query, "imdb result menu", query, "")
    imdb_search_list_item = create_imdb_search_list_item(query);
    imdb_search_tuple = (imdb_search_url, imdb_search_list_item, True)
    return imdb_search_tuple
	
def create_imdb_search_tuple_tv(query):
    imdb_search_url = create_url(query, "imdb result tv menu", query, "")
    imdb_search_list_item = create_imdb_search_list_item(query);
    imdb_search_tuple = (imdb_search_url, imdb_search_list_item, True)
    return imdb_search_tuple
	
def create_imdb_actorsearch_tuple(query):
    imdb_actorsearch_url = create_url(query, "imdb actor result menu", query, "")
    imdb_actorsearch_list_item = create_imdb_actorsearch_list_item(query);
    imdb_actorsearch_tuple = (imdb_actorsearch_url, imdb_actorsearch_list_item, True)
    return imdb_actorsearch_tuple
	
def create_archive_tuple(xbmcname, text, name, mode, url, id, size, poster, imdb_id, type):
    if mode == "t music files menu" or mode == "t music queue menu":
        archive_url = create_url(xbmcname, mode, id, poster)
    else:
        archive_url = create_url(xbmcname, mode, id, imdb_id)
    archive_list_item = create_archive_list_item(xbmcname, text, name, url, id, size, poster, type);
    archive_tuple = (archive_url, archive_list_item, True)
    return archive_tuple
	
def create_file_list_tuple(xbmcname, text, name, mode, url, size, poster, type, imdb_id):
    if LIBRARY_FORMAT:
        if DPD:
            file_list_url = create_url("%s.%s" % (xbmcname,type), mode, url, imdb_id)
        else:
            file_list_url = create_url(xbmcname, mode, url, imdb_id)
    else:
        file_list_url = create_url(name, mode, url, imdb_id)
    file_list_item = create_file_list_item(xbmcname, text, name, url, size, poster, type, imdb_id);
    file_list_tuple = (file_list_url, file_list_item, True)
    return	file_list_tuple
	
def create_download_file_tuple(name, path, type, pct, size):
    download_file_url = create_url(name, "play local", path, "")
    download_file_item = create_download_file_list_item(name, path, type, pct, size);
    download_file_tuple = (download_file_url, download_file_item, True)
    return download_file_tuple
	
def create_savedpeople_tuple(name, imdb_id, photo):
    people_url = create_url(name, "actor movies menu", imdb_id)
    people_item = create_people_list_item(name, imdb_id, photo);
    people_tuple = (people_url, people_item, True)
    return people_tuple
	
def create_dls_tuple(name, size, speed, mode, downloaded, id, seeders, fail_reason):
    dls_url = create_url(name, mode, id, "")
    dls_item = create_dls_list_item(name, size, speed, downloaded, id, seeders, fail_reason);
    dls_tuple = (dls_url, dls_item, True)
    return dls_tuple

def create_url(name, mode, data="", imdb_id=""):
    name = urllib.quote(str(name))
    data = urllib.quote(str(data))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&data=%s&mode=%s&imdb_id=%s' % (name, data, mode, imdb_id)
    return url
	
def create_dls_list_item(name, size, speed, downloaded, id, seeders, fail_reason):
    text = "[%s] %s [%s seeds] %s %s" % (downloaded, speed, seeders, size, name) 
    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    return li
	
def create_furk_search_list_item(query):
    contextMenuItems = []
    #remove furk search
    remove_url = '%s?name=%s&mode=remove furk search' % (sys.argv[0], query)
    contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))

    li = xbmcgui.ListItem(clean_file_name(query, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, True)
    return li 

def create_imdb_search_list_item(query):
    contextMenuItems = []
    #remove furk search
    remove_url = '%s?name=%s&mode=remove imdb search' % (sys.argv[0], query)
    contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))

    li = xbmcgui.ListItem(query)
    li.addContextMenuItems(contextMenuItems, True)
    return li 
	
def create_imdb_actorsearch_list_item(query):
    contextMenuItems = []
    #remove furk search
    remove_url = '%s?name=%s&mode=remove actor search' % (sys.argv[0], query)
    contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))

    li = xbmcgui.ListItem(query)
    li.addContextMenuItems(contextMenuItems, True)
    return li 

iconimage = None
def create_actor_list_item(name, photo, imdb_id, profession):
    contextMenuItems = []
    text = "%s | %s" % (name, profession)
    name = clean_file_name(name, use_blanks=False)
    actor_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add people' % (sys.argv[0], urllib.quote(name), imdb_id, urllib.quote(photo))
    contextMenuItems.append(('Add to People List', 'XBMC.RunPlugin(%s)' % actor_url))
    
    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=True)
    li.setIconImage(photo)
    return li
	
def create_movie_list_item(name, imdb_id, rating, votes):
    contextMenuItems = []
    if mode == "dvd releases menu" and name!="error (visit www.xbmchub.com)":
        listname = clean_file_name(name, use_blanks=False)
    else:
        ratings = '[COLOR cyan]' + "[imdb: %s]" % (rating) + '[/COLOR]'
        if name.find(">>> Next Page")>0 or mode == "similartitles menu" or mode == "similartitles tv menu" or rating == "" or rating == "0" or IMDB_RATING == False:
            listname = clean_file_name(name, use_blanks=False)
        else:
            listname = "%s - %s" % (clean_file_name(name, use_blanks=False), ratings)
    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    name_trailer = clean_file_name(name[:len(name)-7], use_blanks=False).replace("3D","").replace('.','-').replace(':','-').replace('&','and').replace(" ","-").replace("'","-").lower()
    data_trailer = imdb_id
    trailer_url = '%s?name=%s&data=%s&imdb_id=%s&mode=view trailer' % (sys.argv[0], urllib.quote(name_trailer), urllib.quote(data_trailer), urllib.quote(name))
    contextMenuItems.append(('View trailer', 'XBMC.RunPlugin(%s)' % trailer_url))
    contextMenuItems.append(('IMDB users also like...', "XBMC.Container.Update(%s?mode=similartitles menu&name=%s&data=%s&imdb_id=%s)" % (sys.argv[0], urllib.quote(name), "MOV", imdb_id ) ) )
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.yifymovies.hd'):
        name2 = name[:len(data)-7].replace("The ","")        
        contextMenuItems.append(('@Search Yify Movies HD', 'XBMC.Container.Update(%s?action=movies_search&query=%s)' %('plugin://plugin.video.yifymovies.hd/',urllib.quote_plus(name2))))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
        name2 = name[:len(data)-7].replace("The ","")        
        contextMenuItems.append(('@Search Movie 1Channel', 'XBMC.Container.Update(%s?mode=7000&section=&query=%s)' %('plugin://plugin.video.1channel/',name2)))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
        iurl='http%3a%2f%2fwww.icefilms.info%2f'
        name2 = name[:len(data)-7].replace("The ","")
        contextMenuItems.append(('@Search Movie Icefilms', 'Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',iurl,urllib.quote(name2),"0")))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.moviestorm'):
        name2 = name[:len(data)-7].replace("The ","")        
        contextMenuItems.append(('@Search MovieStorm', 'XBMC.Container.Update(%s?mode=7&name=%s&url=%s)' %('plugin://plugin.video.moviestorm/',urllib.quote(name2), "url")))
    if exist_in_dir(clean_file_name(name), MOVIES_PATH, isMovie=True):
        remove_url = '%s?name=%s&data=%s&imdb_id=%s&mode=remove movie strm' % (sys.argv[0], urllib.quote(name), urllib.quote(name), imdb_id)
        contextMenuItems.append(('Remove from XBMC library', 'XBMC.RunPlugin(%s)' % remove_url))
    else:
        add_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add movie strm' % (sys.argv[0], urllib.quote(name), urllib.quote(name), imdb_id)
        contextMenuItems.append(('Add movie to XBMC library', 'XBMC.RunPlugin(%s)' % add_url))
    name_kat = name[:len(name)-7].replace("The ","")
    data_kat = "dummy"
    kat_url = '%s?name=%s&data=%s&imdb_id=%s&mode=search kat daily' % (sys.argv[0], urllib.quote(name_kat), data_kat, imdb_id)
    contextMenuItems.append(('Search latest torrents', 'XBMC.RunPlugin(%s)' % kat_url))
	
    type = "dummy"
    wishlist_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add wishlist' % (sys.argv[0], urllib.quote(name), type, imdb_id)
    contextMenuItems.append(('Add to Wishlist', 'XBMC.RunPlugin(%s)' % wishlist_url))
    name2 = name[:len(data)-7].replace("The ","")  
    li = xbmcgui.ListItem(clean_file_name(listname, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li = set_movie_meta(li, imdb_id, META_PATH)
    
    return li

       
def create_tv_show_list_item(name, imdb_id, rating, votes):
    contextMenuItems = []
    suffix = ""
    ratings = '[COLOR cyan]' + "[imdb: %s]" % (rating) + '[/COLOR]'
    if name.find(">>> Next Page")>0 or mode == "similartitles menu" or mode == "similartitles tv menu" or rating == "" or rating == "0" or IMDB_RATING == False:
        listname = clean_file_name(name, use_blanks=False)
    else:
        listname = "%s - %s" % (clean_file_name(name, use_blanks=False), ratings)
    
    contextMenuItems.append(('TV Show information', 'XBMC.Action(Info)'))
    contextMenuItems.append(('IMDB users also like...', "XBMC.Container.Update(%s?mode=similartitles tv menu&name=%s&data=%s&imdb_id=%s)" % (sys.argv[0], urllib.quote(name).replace(" Mini-Series","").replace(" TV Series","").replace(' TV Special',''), "TV", imdb_id ) ) )
    if exist_in_dir(clean_file_name(name.split('(')[0][:-1]), TV_SHOWS_PATH):
        remove_url = '%s?data=%s&imdb_id=%s&mode=remove tv show strm' % (sys.argv[0], urllib.quote(name), imdb_id)
        contextMenuItems.append(('Remove from XBMC library', 'XBMC.RunPlugin(%s)' % remove_url))
    else:
        add_url = '%s?data=%s&imdb_id=%s&mode=add tv show strm' % (sys.argv[0], urllib.quote(name), imdb_id)
        contextMenuItems.append(('Add TV show to XBMC library', 'XBMC.RunPlugin(%s)' % add_url))
        
    if subscription_index(name, imdb_id) < 0:
        subscribe_url = '%s?name=%s&data=%s&mode=subscribe' % (sys.argv[0], urllib.quote(name), imdb_id)
        contextMenuItems.append(('Subscribe', 'XBMC.RunPlugin(%s)' % subscribe_url))
    else:
        if UNICODE_INDICATORS:
            suffix = u' \u2665'
        else:
            suffix = " (S)"
        unsubscribe_url = '%s?name=%s&data=%s&mode=unsubscribe' % (sys.argv[0], urllib.quote(name), imdb_id)
        contextMenuItems.append(('Unsubscribe', 'XBMC.RunPlugin(%s)' % unsubscribe_url))
        
    li = xbmcgui.ListItem(listname + suffix)
    li.addContextMenuItems(contextMenuItems, True)
    li = set_tv_show_meta(li, imdb_id, META_PATH)
    
    return li
        
def create_season_list_item(name, data, imdb_id, poster, fanart):
    contextMenuItems = []
    data_split = data.split('<|>')
    tv_show_name = data_split[0].replace(" Mini-Series","").replace(" TV Series","").replace(' TV Special','')
    tv_show_name = tv_show_name[:len(tv_show_name)-7]
    season_number = data_split[1]
    show_season = "%s Season %s" % (tv_show_name, season_number)
	
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setProperty("Video", "true")
    li.setProperty("IsPlayable", "true")
    li.setThumbnailImage(poster)
    li.setProperty('fanart_image', fanart)
    return li
	
def create_archive_list_item(xbmcname, text, name, url, id, size, poster, type):
    contextMenuItems = []#browse context menu
    if mode == 'music file menu' or mode == 'music file disc menu' or mode == 'my files audio menu':
        download_music = '%s?name=%s&data=%s&imdb_id=%s&mode=download music' % (sys.argv[0], urllib.quote(xbmcname), url, urllib.quote(name))  
        contextMenuItems.append(('Download Album', 'XBMC.RunPlugin(%s)' % download_music))
        queue_music = '%s?name=%s&data=%s&imdb_id=%s&mode=t music queue menu' % (sys.argv[0], urllib.quote(xbmcname), id, poster)  
        contextMenuItems.append(('Queue Album', 'XBMC.RunPlugin(%s)' % queue_music))
        add_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add audio stream' % (sys.argv[0], urllib.quote(xbmcname), id, urllib.quote(name))
        contextMenuItems.append(('Add album stream to XBMC library', 'XBMC.RunPlugin(%s)' % add_url))
    if SKIP_BROWSE:
        contextMenuItems.append(('Browse archive', "XBMC.Container.Update(%s?mode=browse context menu&name=%s&data=%s&imdb_id=%s)" % (sys.argv[0], urllib.quote(xbmcname), id, imdb_id ) ) )
    if mode == 'my files deleted menu':
        mf_action = '%s?name=%s&data=%s&mode=mf clear' % (sys.argv[0], urllib.quote(name), id)  
        contextMenuItems.append(('Clear deleted file', 'XBMC.RunPlugin(%s)' % mf_action))
    if mode != 'my files menu':
        mf_action = '%s?name=%s&data=%s&mode=mf add' % (sys.argv[0], urllib.quote(name), id)  
        contextMenuItems.append(('Add to My Files', 'XBMC.RunPlugin(%s)' % mf_action))
    if mode == 'my files menu' or text.find('[COLOR gold]')==0:
        mf_action = '%s?name=%s&data=%s&mode=mf remove' % (sys.argv[0], urllib.quote(name), id)  
        contextMenuItems.append(('Remove from My Files', 'XBMC.RunPlugin(%s)' % mf_action))
    mf_action = '%s?name=%s&data=%s&mode=mf protect' % (sys.argv[0], urllib.quote(name), id)  
    contextMenuItems.append(('Protect - My Files', 'XBMC.RunPlugin(%s)' % mf_action))
    if mode == 'my files menu':
        mf_action = '%s?name=%s&data=%s&mode=mf unprotect' % (sys.argv[0], urllib.quote(name), id)  
        contextMenuItems.append(('Unprotect - My Files', 'XBMC.RunPlugin(%s)' % mf_action))
    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    li.setProperty('fanart_image', fanart)
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setThumbnailImage(poster)
    return li
	
def create_file_list_item(xbmcname, text, name, url, size, poster, type, imdb_id):
    contextMenuItems = []
    if imdb_id.find("$")>0:
        spliti = imdb_id.split('$')
        deletei = "%s$%s$%s" % ("down_delete", spliti[1], spliti[2])
    else:
        deletei = imdb_id
    if LIBRARY_FORMAT and mode!="t music vid files menu":
        filename = "%s.%s" % (xbmcname,name[len(name)-3:])
    else:
        filename = name
    if name.endswith("srt"):
        text = '[COLOR cyan]' + text + '[/COLOR]'

    download_only = '%s?name=%s&data=%s&imdb_id=%s&mode=download only' % (sys.argv[0], urllib.quote(filename), url, type)  
    contextMenuItems.append(('Download File', 'XBMC.RunPlugin(%s)' % download_only))		
    if not name.endswith("srt"): 
        if DPD: 
            stream_play = '%s?name=%s&data=%s&imdb_id=%s&mode=execute video' % (sys.argv[0], urllib.quote(filename), url, imdb_id)  
            contextMenuItems.append(('Stream Video', 'XBMC.RunPlugin(%s)' % stream_play))
        download_play = '%s?name=%s&data=%s&imdb_id=%s&mode=download play' % (sys.argv[0], urllib.quote(filename), url, imdb_id)  
        contextMenuItems.append(('Download and Play', 'XBMC.RunPlugin(%s)' % download_play))
        download_play_delete = '%s?name=%s&data=%s&imdb_id=%s&mode=download play delete' % (sys.argv[0], urllib.quote(filename), url, deletei)  
        contextMenuItems.append(('Download, Play & Delete', 'XBMC.RunPlugin(%s)' % download_play_delete))
        if type == "movie":
            add_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add moviefile strm' % (sys.argv[0], urllib.quote(filename), url, imdb_id)
        else:
            add_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add episode strm' % (sys.argv[0], urllib.quote(filename), url, imdb_id)
        contextMenuItems.append(('Add stream to XBMC library', 'XBMC.RunPlugin(%s)' % add_url))

    li = xbmcgui.ListItem(clean_file_name(text, use_blanks=False))
    li.setProperty('fanart_image', fanart)
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setThumbnailImage(poster)
    return li
	
def create_download_file_list_item(name, path, type, pct, size):
    contextMenuItems = []
    if mode != "wishlist pending menu" and mode != "wishlist finished menu":
        delete_file = '%s?name=%s&data=%s&imdb_id=%s&mode=delete download' % (sys.argv[0], urllib.quote(name), size, type)  
        contextMenuItems.append(('Delete File', 'XBMC.RunPlugin(%s)' % delete_file))
    if mode == "wishlist pending menu" or mode == "wishlist finished menu":
        if mode == "wishlist pending menu":
            list_path = WISHLIST
        else:
            list_path = WISHLIST_FINISHED
        list_data = name.replace(" | ", "<|>")
        remove_url = '%s?name=%s&data=%s&mode=remove wishlist search' % (sys.argv[0], urllib.quote(list_data), list_path)
        contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))
    li = xbmcgui.ListItem("%s %s" % (clean_file_name(name.replace("dummy", ""), use_blanks=False), pct))
    li.addContextMenuItems(contextMenuItems, replaceItems=True)
    return li
	
def create_people_list_item(name, imdb_id, photo):
    contextMenuItems = []
    list_path = PEOPLE_LIST
    list_data = "%s<|>%s<|>%s" % (name, imdb_id, photo)
    remove_url = '%s?name=%s&data=%s&mode=remove wishlist search' % (sys.argv[0], urllib.quote(list_data), list_path)
    contextMenuItems.append(('Remove', 'XBMC.RunPlugin(%s)' % remove_url))
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False))
    li.setIconImage(photo)
    li.addContextMenuItems(contextMenuItems, replaceItems=True)
    return li
	
series = None
description = None
blank = None
    
def create_episode_list_item(name, data, imdb_id, poster, title, year, overview, rating, premiered, genre, fanart, easyname):
    contextMenuItems = []
    data_split = data.split('<|>')
    tv_show_name = data_split[0].replace(" Mini-Series","").replace(" TV Series","").replace(' TV Special','').replace("The ","")
    season_number = int(data_split[2])
    episode_number = int(data_split[3])
    season_episode = "s%.2de%.2d" % (season_number, episode_number)
	
    contextMenuItems.append(('TV Show information', 'XBMC.Action(Info)'))
    data1 = str(data).replace('<|>', '$')
	
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
        data = data.split('<|>')
        tv_show_name = data[0].replace(" Mini-Series","")
        contextMenuItems.append(('@Search Tv 1Channel', 'XBMC.Container.Update(%s?mode=7000&section=tv&query=%s)' %('plugin://plugin.video.1channel/',tv_show_name)))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.icefilms'):
        iurl='http%3a%2f%2fwww.icefilms.info%2f'
        iname = "%s %sx%.2d" % (tv_show_name,season_number,episode_number)
        contextMenuItems.append(('@Search Episode Icefilms', 'Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' %('plugin://plugin.video.icefilms/',iurl,urllib.quote(iname),"0")))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.moviestorm'):
        tv_show_name = data_split[0].replace(" Mini-Series","")       
        contextMenuItems.append(('@Search MovieStorm', 'XBMC.Container.Update(%s?mode=7&name=%s&url=%s)' %('plugin://plugin.video.moviestorm/',tv_show_name, "url")))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.tvonline.cc'):
        tv_show_name = data_split[0].replace(" Mini-Series","")       
        contextMenuItems.append(('@Search TVonline', 'XBMC.Container.Update(%s?mode=17&name=%s&url=%s)' %('plugin://plugin.video.tvonline.cc/',tv_show_name, "url")))
    if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.tv4me'):
        tv_show_name = data_split[0].replace(" Mini-Series","")       
        contextMenuItems.append(('@Search TV4ME', 'XBMC.Container.Update(%s?mode=18&name=%s&url=%s)' %('plugin://plugin.video.tv4me/',tv_show_name, "url")))

    name_kat = tv_show_name.replace("The ","")
    data_kat = season_episode
    kat_url = '%s?name=%s&data=%s&imdb_id=%s&mode=search kat daily' % (sys.argv[0], urllib.quote(name_kat), data_kat, imdb_id)
    contextMenuItems.append(('Search latest torrents', 'XBMC.RunPlugin(%s)' % kat_url))
    wishlist_url = '%s?name=%s&data=%s&imdb_id=%s&mode=add wishlist' % (sys.argv[0], urllib.quote(name_kat), data_kat, imdb_id)
    contextMenuItems.append(('Add to Wishlist', 'XBMC.RunPlugin(%s)' % wishlist_url))
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False))
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    li.setProperty("Video", "true")
    li.setProperty("IsPlayable", "true")
    li.setInfo(type='Video', infoLabels={'title': title,
    'year': int(year),
    'genre': genre,
    'plot': overview,
    'rating': float(rating),
    'premiered': premiered})
    li.setThumbnailImage(poster)
    li.setProperty('fanart_image', fanart)

    return li
	
   
def create_movie_directory_list_item(name, mode):
    contextMenuItems = []
    suffix = ""
    
    if subscription_index(name, mode) < 0:
        subscribe_url = '%s?name=%s&data=%s&mode=subscribe' % (sys.argv[0], urllib.quote(name), mode)
        contextMenuItems.append(('Subscribe', 'XBMC.RunPlugin(%s)' % subscribe_url))
    else:
        if UNICODE_INDICATORS:
            suffix = u' \u2665'
        else:
            suffix = " (S)"
        unsubscribe_url = '%s?name=%s&data=%s&mode=unsubscribe' % (sys.argv[0], urllib.quote(name), mode)
        contextMenuItems.append(('Unsubscribe', 'XBMC.RunPlugin(%s)' % unsubscribe_url))

    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False) + suffix, thumbnailImage=os.path.join(ADDON.getAddonInfo('path'), 'art', THEME,mode + '.png'))
    li.setProperty('fanart_image', fanart)
    li.addContextMenuItems(contextMenuItems, replaceItems=False)
    
    return li

def create_directory_list_item(name, mode):
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False),thumbnailImage=os.path.join(ADDON.getAddonInfo('path'),'art',THEME ,mode + '.png'))
    li.setProperty('fanart_image', fanart)
    return li
	
def create_sub_directory_list_item(name, mode):
    li = xbmcgui.ListItem(clean_file_name(name, use_blanks=False),thumbnailImage=os.path.join(ADDON.getAddonInfo('path'),'art',THEME ,name + '.png'))
    li.setProperty('fanart_image', fanart)
    return li

def scan_library():
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')

def clean_library():
    xbmc.executebuiltin('CleanLibrary(video)')

def get_missing_meta(missing_meta, type):
    if len(missing_meta) > 0 and DOWNLOAD_META:
        ADDON.setSetting('disable_dialog', value='DISABLE')
        xbmc.log("[What the Furk...XBMCHUB.COM] Downloading missing %s meta data for %d files..." % (type, len(missing_meta)))
        dlThread = DownloadThread(missing_meta, type)
        dlThread.start()
        xbmc.log("[What the Furk...XBMCHUB.COM] ...meta download complete!")
    
class DownloadThread(Thread):
    def __init__(self, missing_meta, meta_type):
        self.missing_meta = missing_meta
        self.type = meta_type
        Thread.__init__(self)

    def run(self):
        if self.type == 'movies':
            for imdb_id in self.missing_meta:
                download_movie_meta(imdb_id, META_PATH)
        if self.type == 'tv shows':
            for imdb_id in self.missing_meta:
                download_tv_show_meta(imdb_id, META_PATH)
        xbmc.executebuiltin("Container.Refresh")
        ADDON.setSetting('disable_dialog', value='ENABLE')
		
class DownloadMusicThread(Thread):
    def __init__(self, name, url, data_path, album_path):
        self.data = url
        self.path = data_path
        self.extpath = album_path
        Thread.__init__(self)

    def run(self):
        path = str(self.path)
        data = self.data
        extract = str(self.extpath)
        urllib.urlretrieve(data, path)
        notify = "%s,%s,%s" % ('XBMC.Notification(Download finished',clean_file_name(name, use_blanks=False),'4000)')
        xbmc.executebuiltin(notify)
        if mode!="download song":
            notify = "%s,%s,%s" % ('XBMC.Notification(Extracting songs',clean_file_name(name, use_blanks=False),'4000)')
            xbmc.executebuiltin(notify)
            time.sleep(1)
            extractfiles(path,extract)
            os.remove(path)
            notify = "%s,%s,%s" % ('XBMC.Notification(Finished',clean_file_name(name, use_blanks=False),'4000)')
            xbmc.executebuiltin(notify)
		
def extractfiles(filepath, extpath):
    try:
        zipn = zipfile.ZipFile(filepath, 'r')
        zipn.extractall(extpath)
    except Exception, e:
        print str(e)
        return False

    return True

class DownloadFileThread(Thread):
    def __init__(self, name, url, data_path, WAITING_TIME):
        self.data = url
        self.path = data_path
        self.waiting = WAITING_TIME
        Thread.__init__(self)

    def run(self):
        start_time = time.time() + 20 + self.waiting
        waiting = self.waiting
        path = self.path
        data = self.data
        try:
            urllib.urlretrieve(data, path, lambda nb, bs, fs: self._dlhook(nb, bs, fs, self, start_time, path, waiting))
        except:
            if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError):
                time.sleep(2)
                os.remove(path)
                return False 
            else: 
                raise
            return False
        notify = "%s,%s,%s" % ('XBMC.Notification(Download finished',clean_file_name(name, use_blanks=False),'5000)')
        xbmc.executebuiltin(notify)
		
    def _dlhook(self, numblocks, blocksize, filesize, dt, start_time, path, waiting):
        if time.time() > start_time:
            if xbmc.Player().isPlayingVideo() == False and mode != "download play" and mode != "download only":
                print "Stopped playing, stopping download, deleting file"   
                raise StopDownloading('Stopped Downloading')
                callEndOfDirectory = False
		
class DownloadFileThreadTV(Thread):
    def __init__(self, name, url, data_path, WAITING_TIME):
        self.data = url
        self.path = data_path
        self.waiting = WAITING_TIME
        Thread.__init__(self)

    def run(self):
        start_time = time.time() + 3 + self.waiting
        path = self.path
        data = self.data
        try:
            urllib.urlretrieve(data, path, lambda nb, bs, fs: self._dlhook(nb, bs, fs, self, start_time, path))
        except:
            if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError):
                time.sleep(3)
                os.remove(path)
                return False 
            else: 
                raise
            return False
        notify = "%s,%s,%s" % ('XBMC.Notification(Download finished',clean_file_name(name, use_blanks=False),'5000)')
        xbmc.executebuiltin(notify)
		
    def _dlhook(self, numblocks, blocksize, filesize, dt, start_time, path):
        if time.time() > start_time:
            if xbmc.Player().isPlayingVideo() == False and mode != "download play" and mode != "download only":
                print "Stopped playing, stopping download, deleting file"   
                raise StopDownloading('Stopped Downloading')
                callEndOfDirectory = False


def setView(content, viewType):
	# set content type so library shows more views and info
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if ADDON.getSetting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

    	    
def get_menu_items(name, mode, data, imdb_id):
    enable_sort = False
    
    if mode == "main menu": #Main menu
        items = main_menu()
    elif mode == "imdb menu":
        items = imdb_menu()
    elif mode == "imdb tv menu":
        items = imdb_menu_tv()
    elif mode == "search menu":
        items = search_menu()
    elif mode == "imdb list menu":
        items = imdb_list_menu()
    elif mode == "nzbmovie menu":
        items = nzbmovie_menu()
    elif mode == "all movies menu": #all menu
        items, missing_meta = movies_all_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "actor movies menu":
        items, missing_meta = movies_actors_menu(name, data)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT#elif mode == "test":
    elif mode == "dvd release menu": #Genres menu
        items = dvd_release_menu()
    elif mode == "3d menu": #Genres menu
        items = threed_menu()
    elif mode  == "browse context menu":
        items = t_file_dialog_movie(name, data, imdb_id, strm=False)
    elif mode == "dvd releases menu":
        items, missing_meta = dvd_releases(data)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT#
    elif mode == "3d result menu":
        items, missing_meta = threed_releases(data)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "music video menu":
        items = movie_dialog(name,"dummy")
        setView('movies', 'movies-view')
    elif mode == "download movies menu": #all menu
        items = download_movies_menu()
    elif mode == "download episodes menu": #all menu
        items = download_episodes_menu()#
    elif mode == "people list menu":
        items = people_list_menu()
    elif mode == "wishlist pending menu":
        items = wishlist_pending_menu()
    elif mode == "wishlist finished menu": #all menu
        items = wishlist_finished_menu()
    elif mode == "nzbweek menu": 
        items, missing_meta = nzbweek_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "nzbmonth menu": 
        items, missing_meta = nzbmonth_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "nzbyear menu":
        items, missing_meta = nzbyear_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
		
    elif mode == "nzbwatchlist menu": 
        items, missing_meta = nzbwatchlist_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
		
    elif mode == "maintenance menu":
        items = maintenance()
		
    elif mode == "help menu":
        items = help_menu()
		
    elif mode == "help list menu": 
        items = help(name)
		
    elif mode == "download menu":
        items = downloads()

    elif mode == "watchlist menu": #all menu
        items, missing_meta = watchlist_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list1 menu": #all menu
        items, missing_meta = list1_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list2 menu": #all menu
        items, missing_meta = list2_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list3 menu": #all menu
        items, missing_meta = list3_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list4 menu": #all menu
        items, missing_meta = list4_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list5 menu": #all menu
        items, missing_meta = list5_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list6 menu": #all menu
        items, missing_meta = list6_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list7 menu": #all menu
        items, missing_meta = list7_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list8 menu": #all menu
        items, missing_meta = list8_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list9 menu": #all menu
        items, missing_meta = list9_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "list10 menu": #all menu
        items, missing_meta = list10_menu()
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "watchlist tv menu": #Genre menu
        items, missing_meta = watchlist_tv_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "movie mpaas menu": #Genres menu
        items = movies_mpaas_menu()
    elif mode == "movie mpaa menu": #Genre menu
        items, missing_meta = movies_mpaa_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "movie genres menu": #Genres menu
        items = movies_genres_menu()
    elif mode == "movie genre menu": #Genre menu
        items, missing_meta = movies_genre_menu(data, str(imdb_id).lower())
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "movie groups menu": #Groups menu
        items = movies_groups_menu()
    elif mode == "movie group menu": #Group menu
        items, missing_meta = movies_group_menu(data, str(imdb_id).lower())
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "movie studios menu": #Studios menu
        items = movies_studios_menu()
    elif mode == "movie studio menu": #Studio menu
        items, missing_meta = movies_studio_menu(data, str(imdb_id).lower())
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "new movies menu": #New movies menu
        items, missing_meta = movies_new_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "movies soon menu": #Coming Soon
        items, missing_meta = movies_soon_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "blu-ray menu": #blu-ray
        items, missing_meta = blu_ray_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "similartitles menu":
        items, missing_meta = imdb_similar_menu(name, data, imdb_id)
        get_missing_meta(missing_meta, 'movies')
        setView('movies', 'movies-view')
        enable_sort = XBMC_SORT
    elif mode == "similartitles tv menu":
        items, missing_meta = imdb_similar_menu(name, data, imdb_id)
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "all tv shows menu": #all menu
        items, missing_meta = tv_shows_all_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "tv show genres menu": #Genres menu
        items = tv_shows_genres_menu()
    elif mode == "tv show genre menu": #Genre menu
        items, missing_meta = tv_shows_genre_menu(data, str(imdb_id).lower())
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "tv show groups menu": #Groups menu
        items = tv_shows_groups_menu()
    elif mode == "tv show group menu": #Group menu
        items, missing_meta = tv_shows_group_menu(data, str(imdb_id).lower())
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "active tv shows menu": #New movies menu
        items, missing_meta = tv_shows_active_menu(data, imdb_id)
        get_missing_meta(missing_meta, 'tv shows')
        setView('movies', 'tvshows-view')
        enable_sort = XBMC_SORT
    elif mode == "music file menu": 
        items = music_dialog(name, data, imdb_id)
    elif mode == "music file disc menu": 
        items = music_dialog(name, data, imdb_id)
    elif mode == "context artist menu":
        items = music_dialog(name, "", imdb_id)
    elif mode == "episodes menu":
        items = tv_shows_episodes_menu(data, imdb_id)
        setView('movies', 'episodes-view')
    elif mode == "seasons menu":
        items = tv_shows_seasons_menu(name, imdb_id)
        get_missing_meta(imdb_id, 'tv shows')
    elif mode == "my files directory menu":
        items = myfiles_directory()
    elif mode == "my files menu":
        items = myfiles(unlinked='0')
    elif mode == "my files audio menu":
        items = myfiles_audio(unlinked='0')
    elif mode == "my files deleted menu":
        items = myfiles(unlinked='1')
    elif mode == "movie result menu":
        if len(imdb_id)>0:
            items = movie_dialog(name, imdb_id)
    elif mode == "episode result menu":
        if len(imdb_id)>0:
            items = episode_dialog(data, imdb_id)
    elif mode == "t files menu":
        items = t_file_dialog_movie(name, data, imdb_id)#
    elif mode == "t music vid files menu":
        items = t_file_dialog_movie(name, data, imdb_id)
    elif mode == "t music files menu":
        items = t_file_dialog_music(name, data, imdb_id, True)
    elif mode == "t music queue menu":
        items = t_file_dialog_music(name, data, imdb_id, False)
    elif mode == "t files tv menu":
        items = t_file_dialog_movie(name, data, imdb_id)
    elif mode == "subscription menu": #Subscription menu
        items = subscription_menu()
    elif mode == "furk search menu": #Search menu
        items = furk_search_menu()
    elif mode == "imdb search menu": #Search menu
        items = imdb_search_menu()
    elif mode == "imdb search tv menu": #Search menu
        items = imdb_search_menu_tv()
    elif mode == "imdb result menu":
        items, missing_meta = imdb_result_menu(name)
        #get_missing_meta(missing_meta, 'movies')
    elif mode == "imdb result tv menu":
        items, missing_meta = imdb_result_menu_tv(data)
        #get_missing_meta(missing_meta, 'tv shows')
    elif mode == "imdb actor menu": #Search menu
        items = imdb_actor_menu()
    elif mode == "imdb actor result menu":
        items = imdb_actor_result_menu(data)
    elif mode == "furk result dialog menu":
        items = furksearch_dialog(data)
    elif mode == "active download menu":
        items = get_downloads(dl_status='active')
    elif mode == "failed download menu":
        items = get_downloads(dl_status='failed')
    elif mode == "music menu":
        items = music_menu()
    elif mode == "ukofficial menu":
        items = music_lists(data)
    elif mode == "billboard menu":
        items = music_lists(data)
    elif mode == "search artist menu":
        items = search_artist()
    elif mode == "search album menu":
        items = search_artist()
    elif mode == "chart menu":
        items = chart_menu()
    elif mode == "discography menu":
        items = discography(name,data,imdb_id)
    else:
        items = []
        
    if enable_sort:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)      
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    try:
        return items
    except:
        pass

#Other

def get_params(paramstring):
    param = {}
    if len(paramstring) >= 2:
        paramstring = paramstring.replace('?', '')
        pairsofparams = paramstring.split('&')
        for p in pairsofparams:
            splitparams = p.split('=')
            if len(splitparams) == 2:
                param[splitparams[0]] = splitparams[1]            
    return param


params = get_params(sys.argv[2])

try:
    name = urllib.unquote_plus(params["name"])
except:
    name = ""
try:
    data = urllib.unquote_plus(params["data"])
except:
    data = ""
try:
    imdb_id = urllib.unquote_plus(params["imdb_id"])
except:
    imdb_id = ""
try:
    mode = urllib.unquote_plus(params["mode"])
except:
    mode = "main menu"

xbmc.log("[What the Furk...XBMCHUB.COM] mode=%s     name=%s     data=%s     imdb_id=%s" % (mode, name, data, imdb_id))

if mode.endswith('menu'):
    items = get_menu_items(name, mode, data, imdb_id)
    try:
        xbmcplugin.addDirectoryItems(int(sys.argv[1]), items, len(items))
    except:
        pass

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    dev_message()
    

elif mode == "strm file dialog":
    li = xbmcgui.ListItem(name)
    execute_video(name, data, imdb_id, strm=True)
elif mode == "strm movie dialog":
    strm_movie_dialog(name, imdb_id, strm=False)
elif mode == "strm tv show dialog":
    strm_episode_dialog(data, imdb_id, strm=False)
elif mode == "play":
    execute_video(name, imdb_id)
elif mode == "remove furk search":
    remove_search_query(name, FURK_SEARCH_FILE)
    xbmc.executebuiltin("Container.Refresh")
elif mode == "remove imdb search":
    remove_search_query(name, IMDB_SEARCH_FILE)
    xbmc.executebuiltin("Container.Refresh")
	
elif mode == "remove actor search":
    remove_search_query(name, IMDB_ACTOR_FILE)
    xbmc.executebuiltin("Container.Refresh")
	
elif mode == "remove wishlist search":
    remove_search_query(name, data)
    xbmc.executebuiltin("Container.Refresh")

elif mode == "subscribe":
    subscribe(name, data)
    xbmc.executebuiltin("Container.Refresh")
elif mode == "delete cache":
    deletecachefiles()
elif mode == "delete meta zip":
    deletemetazip()
elif mode == "delete search lists":
    deletesearchlists()
elif mode == "delete packages":
    deletepackages()
elif mode == "delete wishlists":
    deletewishlists()
elif mode == "delete metafiles":
    deletemetafiles()
elif mode == "move metafiles":
    move_meta()
elif mode == "account info":
    account_info()

elif mode == "unsubscribe":
    if name.find('[') >= 0:
        name = name.split('[')[0][:-1]
    unsubscribe(name, data)
    xbmc.executebuiltin("Container.Refresh")
elif mode == "get subscriptions":
    get_subscriptions()
elif mode == "force subscriptions":
    ADDON.setSetting('service_time', str(datetime.datetime.now()).split('.')[0])
    time.sleep(2)
    get_subscriptions()
    hours_list = [2, 5, 10, 15, 24]
    hours = hours_list[settings.subscription_timer()]
    ADDON.setSetting('service_time', str(datetime.datetime.now() + timedelta(hours=hours)).split('.')[0])
    time.sleep(1)
    xbmc.executebuiltin("Container.Refresh")
    
elif mode == "add movie strm":
    create_strm_file(name, data, imdb_id, "strm movie dialog", MOVIES_PATH)
elif mode == "add moviefile strm":
    create_strm_file(name, data, imdb_id, "strm file dialog", MOVIES_PATH)
    scan_library()
elif mode == "add episode strm":
    create_strm_file(name, data, imdb_id, "strm file dialog", TV_SHOWS_PATH)
elif mode == "one-click on":
    ADDON.setSetting('oneclick_search', value='true')
    xbmc.executebuiltin("Container.Refresh")
elif mode == "one-click off":
    ADDON.setSetting('oneclick_search', value='false')
    xbmc.executebuiltin("Container.Refresh")
elif mode == "remove movie strm":
    remove_strm_file(data, MOVIES_PATH)
elif mode == "add tv show strm":
    data = clean_file_name(data.split('(')[0][:-1])
    create_tv_show_strm_files(data, imdb_id, "strm tv show dialog", TV_SHOWS_PATH)

elif mode == "remove tv show strm":
    data = clean_file_name(data.split('(')[0][:-1])
    remove_tv_show_strm_files(data, TV_SHOWS_PATH)
	
elif mode == "seasonsearch":
    season_dialog(name, imdb_id)
	
elif mode == "mf add":
    myfiles_add(name, data)
	
elif mode =="mf clear":
    myfiles_clear(name, data)
	
elif mode == "mf remove":
    myfiles_remove(name, data)
	
elif mode == "mf protect":
    myfiles_protect(name, data)
	
elif mode == "mf unprotect":
    myfiles_unprotect(name, data)
	
elif mode == "download play":
    download_play(name, data, imdb_id)
	
elif mode == "download play delete":
    print "mode - " + imdb_id
    download_play(name, data, imdb_id)

elif mode == "download only":
    download_only(name, data, imdb_id)
	
elif mode == "download music":
    download_music(name, data, imdb_id)
	
elif mode == "download song":
    download_music(name, data, imdb_id)
	
elif mode == "execute video":
    execute_video(name, data, imdb_id, strm=False)
	
elif mode == "add download":
    add_download(name, data)#
	
elif mode == "play local":
    xbmcplay(data)
	
elif mode == "delete download":
    delete_download(name, data, imdb_id)
	
elif mode == "scan library":
    scan_library()
	
elif mode == "search kat daily":
    download_kat(name, data)
	
elif mode == "wishlist search":
    one_click_download()
	
elif mode == "add wishlist":
    add_wishlist(name, data)
	
elif mode == "add people":
    add_people(name, data, imdb_id)
	
elif mode == "refresh list":
    xbmc.executebuiltin("Container.Refresh")
	
elif mode == "toggle one-click":
    toggle_one_click()
	
elif mode == "dev message":
    ADDON.setSetting('dev_message', value='run')
    dev_message()
	
elif mode == "view trailer":
    view_trailer(name, data, imdb_id)
	
elif mode == "add audio stream":
    add_audio_stream(name, data, imdb_id)
	
elif mode == "enable pc setting":
    pc_setting()
	
elif mode == 'test download':
    test_dl_speed()
	
elif mode == "setup wizard":
    setup_FURK()
		

	

	

	

	

	


	





	



  
	

