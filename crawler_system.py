import urllib2, urllister, urlparse, re, sys, socket

sys.setrecursionlimit(2000)

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
        result.status = code
        return result

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result
    
class CrawlerSys:

    # Crawler function searches for urls of interest
    # self: default parameter
    # url is the initial url
    # visited_urls: list where the visited urls are stored 
    # f: file where the visited_urls list is stored 
    def crawler(self, url, visited_urls, temp, f):

        if len(visited_urls)>=1100:
            return

        print len(visited_urls)
        
        o = urlparse.urlsplit(url)
        #print url
        #print o.scheme
        
        if url.startswith("http"):
            temp = url
    ##    elif url.startswith("/"):
    ##        print "lala"
    ##        return
    ##        url = temp + url
        else:
            return

        request = urllib2.Request(url)
        opener = urllib2.build_opener(SmartRedirectHandler(), DefaultErrorHandler())
        parser = urllister.URLLister()
        try:
            datastream = opener.open(request, timeout=2)
        except IOError:
            print "Error"
            return
        
        #print datastream.info().getsubtype()
        if datastream.info().getsubtype() == 'html':
            try:
                raw = datastream.read()
            except socket.error:
                errno, errstr = sys.exc_info()[:2]
                if errno == socket.timeout:
                    print "There was a timeout"
                else:
                    print "There was some other socket error"
                return
            
            #print len(raw)
            if len(raw) > 40000:
                #print url
                #print len(visited_urls)
                
                parser.feed(raw)
                datastream.close()
                parser.close()
                visited_urls.append(url)
                f.write(url + "\n")
            
                for url in parser.urls:
                    if url in visited_urls:
                        #print 'already'
                        continue
                    else:
                        if re.search('\.(acm)\.(org)|\.(gov)|\.(gr)|\.(php)|twitter|wikipedia|@|\?', url):
                            #print 'forbidden'
                            continue
                        elif re.search('\.(com)',url):
                            # Anadromiki klisi tou crawler
                            self.crawler(url, visited_urls, temp, f)
                        else:
                            continue
            else:
                datastream.close()
                parser.close()
        else:
            datastream.close()
            parser.close()
