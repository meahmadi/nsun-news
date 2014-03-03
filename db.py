import sqlite3
import uuid

class DB(object):
    def __init__(self):
        self.tmp_db = None
        self.conf_db=None
        self.person_db = None
        self._idx = 0
    

    def init_dbs(self):
        self.tmp_db = sqlite3.connect('news.db')#:memory:
        self.conf_db = sqlite3.connect('conf.db')
        self.person_db = sqlite3.connect('person.db')
        
    def init_schemas(self):
        self.tmp_db.execute("create table if not exists news_val(fetchid text, newsid text, idx integer, name text, value text);")
        self.tmp_db.execute("create table if not exists fetch_val(feedid text, fetchid text, idx integer, name text, value text);")
        
        self.conf_db.execute("create table if not exists feed(feedid text, name text, url text, description text);")
                            
        self.person_db.execute("create table if not exists key(keyid text, name text);")
        self.person_db.execute("create table if not exists tag(objid text, keyid text, objtype text);")
        
        self.person_db.execute("create table if not exists favorites(objid text, objtype text, objvalue text, keys text, time datetime);")

    def guid(self):
        return str(uuid.uuid4())
    def idx(self):
        self._idx = self._idx + 1
        return self._idx

    def save_feed(self,name,url,description):
        feedid = self.guid()
        self.conf_db.execute("insert into feed(feedid,name,url,description) values (?,?,?,?);",[feedid,name,url,description])
        self.conf_db.commit()
        return feedid
    
    def get_feeds(self):
        cur = self.conf_db.cursor()
        cur.execute("select feedid,name,url,description from feed;")
        result = []
        for row in cur.fetchall():
            result.append([cell for cell in row])
        return result
            
        
    def save_fetch(self,feedid,fetch):
        fetchid = self.guid()
        for key in fetch.keys():
            query = 'insert into fetch_val (feedid,fetchid,idx,name,value) values ("%s","%s",%d,"%s","%s")'%(feedid,fetchid,self.idx(),key,fetch[key])
            self.tmp_db.execute(query)    
        self.tmp_db.commit()
        return fetchid

    def get_fetch_val(self,fetchid,key):
        cur = self.tmp_db.cursor()
        cur.execute("select * from fetch_val where fetchid=? and name=?;",[fetchid,key])
        result = []
        for row in cur.fetchall():
            result.append([cell for cell in row])
        return result
        
    def save_news(self,fetchid,news):
        newsid = self.guid()
        for key in news.keys():
            try:
                self.tmp_db.execute('insert into news_val (fetchid,newsid,idx,name,value) values ("%s","%s",%d,"%s","%s")'%(fetchid,newsid,self.idx(),str(key).replace("\"","\\\""),str(news[key]).replace("\"","\\\"")))
            except:
                pass
        self.tmp_db.commit()
        return newsid

    def get_news_val(self,newsid,key):
        cur = self.tmp_db.cursor()
        cur.execute("select * from news_val where newsid=? and name=?;",[newsid,key])
        result = []
        for row in cur.fetchall():
            result.append([cell for cell in row])
        return result