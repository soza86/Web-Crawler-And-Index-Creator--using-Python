import crawler_system, tokenize_system, os, re, urlparse, math, time
from xml.etree import ElementTree

# Urls the crawler uses at the beginning 
start = ["http://www.technewsworld.com", "http://www.arstechnica.com", "http://www.wired.com", "http://news.cnet.com", "http://www.anandtech.com"]

visited = [start[0]]

## Start Crawling
craw = crawler_system.CrawlerSys()

f = open('C:\\project\\visited.txt','w')
for u in start:
        craw.crawler(u, visited, u, f)

f.close()

texts_dict = {}

visited.remove(visited[0])

# Tokenize the collection's text
tok = tokenize_system.Tokenizer()
tok.tokenizeUrls(visited)

# Function for removing multiple appearance of a value from a list
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

for u in visited:
        
        # Morphosyntactic analysis using tree-tagger
        tagger_path="C:\\TreeTagger\\bin\\tree-tagger.exe" 
        parameter_file="C:\\TreeTagger\\lib\\english.par"

        filepath = "C:\\project\\Tokens\\Tokens"+ str(visited.index(u)) +".txt"
        targetfile = "C:\\project\\Tokens\\" + str(visited.index(u)) + "_out.txt"
         
        f=os.popen(tagger_path + " -token -lemma -no-unknown \"" + parameter_file + '\" \"' + filepath + '\" \"' + targetfile,'r')
         
        tagged=f.read() 
        f.close()

# Start of timer for counting the time for the construction of the index 
t0 = time.clock()
        
for u in visited:

        targetfile = "C:\\project\\Tokens\\" + str(visited.index(u)) + "_out.txt" 

        # Tagged tokens are processed 
        x = []
        f = open(targetfile, "r")
        x = f.readlines()
        f.close()

        # Removing terminal words
        for i in x:
                if re.search('\tCD\t|\tCC\t|\tDT\t|\tEX\t|\tIN\t|\tLS\t|\tMD\t|\tPDT\t|\tPOS\t|\tPRP\t|\tPRP$\t|\tRP\t|\tTO\t|\tUH\t|\tWDT\t|\tWP\t|\tWP$\t|\tWRB\t|\t,\t|\t:\t|\t''\t|\tSYM\t|t``\t|\tSENT\t', i):
                        #print i
                        x = remove_values_from_list(x,i)


        # Find unique lemmas and the frequency of their appearance
        unique_text = {}

        for i in x:
                temp = i.split('\t')
                k = (temp[2].split('\n'))[0]

                #key = to limma, value = syxnotita emfanisis sto keimeno
                if k in unique_text:
                        unique_text[k] = unique_text[k]+1
                        continue
                else:
                        unique_text[k] = 1

        texts_dict[u] = unique_text

# Find all the unique lemmas in a collection of text
# and the acutal text where they are located to

total_limmata={}

for e in texts_dict:
        limmata = texts_dict[e]
        for l in limmata:
                if l in total_limmata:
                        total_limmata[l].append(e)
                else:
                        total_limmata[l] = [e]

inv_index = {}
# Counting weights and creation of inversed index 
for limma in total_limmata:
        docum = total_limmata[limma]
        w = {}
        for doc in docum:
                td = float((texts_dict[doc])[limma])/float(len(texts_dict[doc]))
                idf = math.log(float(len(texts_dict))/float(len(texts_dict[doc])))
                w[doc] = td*idf

        inv_index[limma] = w

# Creating xml file that contains the inversed index
root = ElementTree.Element("inverted_index")

for i in inv_index:

    lim = ElementTree.SubElement(root, 'lemma', {'name':i})

    docs = inv_index[i]

    for d in docs:
        doc = ElementTree.SubElement(lim, 'document', {'id':str(d), 'weight':str(docs[d])})

tree = ElementTree.ElementTree(root)

# End of timer
print "Xronos kataskeuis eurethriou: "
print time.clock() - t0, "seconds process time"

# Storing the index
tree.write("inverted_index.xhtml")


