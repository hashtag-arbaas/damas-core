import aiohttp
import json
from re import search
import requests
import asyncio 
import socketio 

class http_connection( object ) :
    '''
    Methods to interact with a remote DAMAS server using HTTP
    '''
    def __init__( self, url ) :
        #self.cj = cookielib.LWPCookieJar()
        self.serverURL = url
        self.token = None
        self.headers = {}
    
    def callback(self):
        return None
    
    async def create( self, keys, callback) :
        '''
        Create a node wearing the specified keys
        @param {Hash} keys of the new node
        @returns {Hash} New node on success, false otherwise
        '''
        # def callback(r):
        #     if r.status_code == 201 or r.status_code == 207:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)

        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+"/api/create/", data=json.dumps(keys), headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)

    async def read( self, id_, callback) :
        '''
        Retrieve a node specifying its internal node index
        @param {String} id_ the internal node index to search
        @returns {Hash} node or false on failure
        '''
        # def callback(r):
        #     if r.status_code == 200 or r.status_code == 207:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)
            
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+"/api/read/", data=json.dumps(id_),headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)

    async def update( self, keys, callback) :
        '''
        Modify a node(s). Specifying a None value for a key will
        remove the key from the node.
        @param {Hash} keys of the node to update
        @returns {Hash} updated node or false on failure
        '''
        # def callback(r):
        #     if r.status_code == 200 or r.status_code == 207:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)
            
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+'/api/update/', data=json.dumps(keys), headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)

    async def upsert( self, keys, callback) :
        '''
        Create a node wearing the specified keys or update an already
        existing node if id is specified and found
        @param {Hash} keys of the new node or updated node
        @returns {Hash} New nodes and updated nodes on success, false otherwise
        '''
        # def callback(r):
        #     if r.status_code == 200 or r.status_code == 201:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)
            
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+'/api/upsert/', data=json.dumps(keys),headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)

    async def delete( self, id_, callback) :
        '''
        Delete a node
        @param {String} id_ the internal node index to delete
        @returns {Boolean} True on success, False otherwise
        '''
        # def callback(r):
        #     if r.status_code == 200 or r.status_code == 207:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)
            
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+'/api/delete/', data=json.dumps(id_),headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)

    async def search( self, query, callback) :
        '''
        Find elements wearing the specified key(s)
        @param {String} query string
        @returns {Array} array of element indexes or None if no element found
        '''
        # def callback(r):
        #     if r.status_code == 200:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)
            
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.get(self.serverURL+'/api/search/'+query, headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)        

    async def search_one( self, query, callback) :
        '''
        Find nodes wearing the specified key(s) and return the first occurence
        @param {String} query string
        @returns {Array} array of element indexes or None if no element found
        '''
        # def callback(r):
        #     if r.status_code == 200:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)
            
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.get(self.serverURL+'/api/search_one/'+query, headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)        

    async def search_mongo( self, query, sort, limit, skip, callback) :
        # def callback(r):
        #     if r.status_code == 200:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)
            
        async with aiohttp.ClientSession() as session:
            try:
                data = {"query":query, "sort":sort, "limit":limit, "skip":skip}
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+'/api/search_mongo/', data=json.dumps(data), headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)       

    async def graph( self, id_, callback) :
        '''
        Retrieve a node graph specifying its index
        @param {String} id_ the node index(es) to search
        @returns {Hash} node or false on failure
        '''
        # def callback(r):
        #     if r.status_code == 200 or r.status_code == 207:
        #         return (r.status_code, json.loads(r.text))
        #     return (r.status_code, r.text)
            
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+'/api/graph/0/', data=json.dumps(id_), headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        return callback(res)              

    # USERS AUTHENTICATION METHODS

    async def signIn( self, username, password, callback):
        '''
        @return {Boolean} True on success, False otherwise
        '''
        def req_callback(r):
            if r.status_code == 200:
                self.token = json.loads(r.text)
                self.headers['Authorization'] = 'Bearer ' + self.token['token']
                return (r.status_code, True)
            return (r.status_code, False)
            
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+'/api/signIn/', data={"username":username, "password":password}, headers=headers) as resp:
                    res = await resp.json()
            except Exception:
                return (500, "Connection error")
        if not callback:
            return req_callback(res)     
        return callback(res)

    def signOut( self, callback) :
        '''
        @return {Boolean} True on success, False otherwise
        '''
        self.token =  None
        del self.headers['Authorization']
        if callback:
            return callback()

    async def verify(self, callback=None) :
        '''
        @return {dict} a dictionary containing username and userclass on success, None otherwise
        '''
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.serverURL+'/api/verify/', headers=self.headers) as resp:
                    res = await resp.json()
            except:
                return (500, "Connection error")
        # r = requests.get(self.serverURL+'/api/verify/', headers=self.headers, verify=False )
        if callback:
            return callback(res != None)
        else:
            return res != None
        # if r.status_code == 200:
        #     return (r.status_code, True)
        # return (r.status_code, False)

    # DIGITAL ASSET MANAGEMENT EXTENSION

    async def lock( self, id_,callback) :
        '''
        Lock an asset for edition
        @param {String} id_ the internal node index
        @returns {Boolean} True on success, False otherwise
        '''
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.put(self.serverURL+'/api/lock/', data=json.dumps(id_), headers=headers) as resp:
                    res = await resp.json()
            except:
                return (500, "Connection error")
        if callback:
            return callback(res != None)
        else:
            return res != None
        # if r.status_code == 200:
        #     return (r.status_code, True)
        # return (r.status_code, False)

    async def publish( self, keys, callback) :
        '''
        Publish an asset node wearing the specified keys. The keys _id, comment,
        origin must be specified. _id must be a string starting with '/'
        @param {Hash} keys of the new node
        @returns {Hash} New node on success, false otherwise
        '''
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+'/api/publish/', data=json.dumps(keys), headers=headers) as resp:
                    res = await resp.json()
            except:
                return (500, "Connection error")
        return callback(res)
        # headers = {'content-type': 'application/json'}
        # headers.update(self.headers)
        # r = requests.post(self.serverURL+'/api/publish/', data=json.dumps(keys),
        # headers=headers, verify=False)
        # if r.status_code == 201 or r.status_code == 207:
        #     return (r.status_code, json.loads(r.text))
        # return (r.status_code, r.text)

    async def unlock( self, id_, callback) :
        '''
        Unlock a locked asset
        @param {String} id_ the internal node index
        @returns {Boolean} True on success, False otherwise
        '''
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.put(self.serverURL+'/api/unlock/', data=json.dumps(id_), headers=headers) as resp:
                    res = await resp.json()
            except:
                return (500, "Connection error")
        if callback:
            return callback(res != None)
        else:
            return res != None

    async def version( self, id_, keys, callback) :
        '''
        Create a node version
        @param {Hash} keys of the new node
        @returns {Hash} New node on success, false otherwise
        '''
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post('%s/api/version/%s' % (self.serverURL, id_), data=json.dumps(keys), headers=headers) as resp:
                    res = await resp.json()
            except:
                return (500, "Connection error")
        return callback(res)

    async def comment(self, keys, callback) :
        '''
        Create a node with the specified keys (similar to create
        but concerns child node with parent's id as key)
        @param {Hash} keys of the new node
        @returns {Hash} New node on success, false otherwise
        '''
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'content-type': 'application/json'}
                headers.update(self.headers)
                async with session.post(self.serverURL+"/api/comment/", data=json.dumps(keys), headers=headers) as resp:
                    res = await resp.json()
            except:
                return (500, "Connection error")
        return callback(res)



