import urllib2, nltk, urlparse

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

class Tokenizer():

    # self: default parameter
    # visited_urls: list with the urls from which we extract the text
    def tokenizeUrls(self,visited_urls):

        html_len = 0
        clean_len = 0

        for u in visited_urls:
            #print visited_urls

            #Start of text-dowloading from urls procedure 
            request = urllib2.Request(u)
            opener = urllib2.build_opener(SmartRedirectHandler(), DefaultErrorHandler())
            try:
                datastream = opener.open(request, timeout=2)
            except IOError:
                print "Error"
                visited_urls.remove(u)
                continue
        
            try:
                raw = datastream.read()
            except socket.error:
                errno, errstr = sys.exc_info()[:2]
                if errno == socket.timeout:
                    print "There was a timeout"
                    visited_urls.remove(u)
                else:
                    print "There was some other socket error"
                    visited_urls.remove(u)
                continue

            #print datastream
            
            datastream.close()
            #print len(raw)
            html_len = html_len + len(raw)

            # Production of clean text, using nltk
            pure = nltk.clean_html(raw)

            clean_len = clean_len + len(pure)

            # Write the clean text in the file f 
            f = open('C:\\project\\html_texts\\' + str(visited_urls.index(u)) +'.txt', 'w')
            f.write(pure)
            f.close()
            
            #print pure

            # Producing tokenized text using nltk 
            tokens = nltk.word_tokenize(pure)
            #print tokens

            # Write tokenized text in a file 
            f = open("C:\\project\\Tokens\\Tokens"+ str(visited_urls.index(u)) + ".txt","w")
            for t in tokens:
                f.write(t + "\n")
            f.close()

        # Counting average size of the text collections
        if len(visited_urls)!=0:
            print 'Average size of text collection in characters= ' + str(float(html_len)/float(len(visited_urls)))
            print 'Average size of clean text collection in characters= ' + str(float(clean_len)/float(len(visited_urls)))
        


