from xml.etree import ElementTree

class xmlSys:

    def create_xml_index(self, inv_index):
        
        root = ElementTree.Element("inverted_index")
        #print inv_index

        for i in inv_index:

            lim = ElementTree.SubElement(root, 'lemma', {'name':i})

            docs = inv_index[i]

            for d in docs:
                doc = ElementTree.SubElement(lim, 'document', {'id':str(d), 'weight':str(docs[d])})

        tree = ElementTree.ElementTree(root)
        tree.write("inverted_index.xhtml")
