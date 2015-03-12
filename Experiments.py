from xml.etree import ElementTree

var = raw_input("Enter queries separated with commas:")
if var == "":
    print "No lemma. Exiting..."
else:
    queries = var.split(",")
    print queries
    
    t0 = time.clock()

    x = ElementTree.parse("inverted_index.xhtml")
    lemmas = x.findall("lemma")
    #print lemmas

    for q in queries:
        res = {}
        index = {}
        #print q
        for l in lemmas:
            #print l
            attr = l.items()
            #print attr[0][1]
            if q == attr[0][1]:
                docs = l.getchildren()
                for d in docs:
                    print d.items()
                    p = d.items()
                    res[p[0][0]] = p[0][1]
                    index[q]=res
        print index

    print time.clock() - t0, "seconds process time"
