# Web-Crawler-And-Index-Creator--using-Python

1st Subsystem:  Web Crawler
Web crawler is implemented on the crawler_system.pyfile. Function crawler, which is recursive, is called until the number of 
pages is 1100. For each url, therearesomerestrictions. First, the only accepted urls are with the domain .com; 
secondly the content of the sites is of .html type and finally, the crawler does not allow visits to the same websites, 
by checking the visited_urls list.

2nd Subsystem: Preprocessing
Preprocessing subsystem extracts the clean text from the visited_urls and applies tokenization. 
It is implemented in tokenize_system.py file, using tokenize Urls function.

3rd Subsystem: Morphosyntactic Analysis
This subsystem is implemented in the main.py file, where the tree-tagger tool is used.   

4thSubsystem:Websiterepresentationinthe Vector Space Model
This subsystem is implemented int he main.pyfile. Terminal words are removed from the morphosyntactic texts, 
based on the closed class categories provided in sitehttp://www.infogistics.com/tagset.htmland 
with the use of regular expressions. 

5th Subsystem: Creation of an index
This subsystem creates an inversed index, where all the unique lemmas are located and also the text where each lemma 
is located to. A 2 dimensiondictionaryisused, where key is the id of the text and value is the dictionary with the 
unique lemmas of the text. Finally, for each lemma, the TD-IDF weight is calculated and the respective 
insert in the reversed index is created. 

6thSubsystem:Storing the index
Withthexml_system.pyfile, an xmlfile is created where we store the inversed index.The creation of the xml file is 
done with the use of modulexml.etree.ElementTree. For retrieving the index, 
we use the statement xml.etree.ElementTree.parse("inverted_index.xhtml").

7thEvaluation
Forevaluatingtheproject, weusetheExperiments.py file.Theprogramasksforinputfromtheuser. 
If the user enters nothing, the program ends. 
Else, the reversed index(x = ElementTree.parse("inverted_index.xhtml")) is loaded and in that index the search 
for the user-input lemmas is conducted.  


