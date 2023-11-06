from disk_struct import Disk
from page_replacement_algorithm import  page_replacement_algorithm
from priorityqueue import priorityqueue
from CacheLinkedList import CacheLinkedList
import time
import numpy as np
import heapq
# import matplotlib.pyplot as plt
import os
from io import BytesIO as StringIO
import math
from scipy.spatial import distance
from sklearn.decomposition import NMF
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.

class page_infos():
    def __init__(self, id, time):
       
        self.id = id
        self.frq= {}
        self.dist= {}
        self.frq[id] = 1
        self.dist[id] = time

    def update (self, id, time):
        self.frq[id] = self.frq[id] + 1
        self.dist[id] =  time

 

class nmf(page_replacement_algorithm):

    def __init__(self, param):

        self.N = int(param)
        np.random.seed(123)
        self.time = 0

        
        self.pages = []
        self.unique_pages = set()
        self.seq_len = self.N
        self.pages_infos = {}
        self.page_freq = {}
        self.page_dist = {}

    def page_distances(self, pg1 , pg2):   
        ind = self.pages.index(pg1)
        counter, frequency, cum_counter = 0, 0, 0
        for j in self.pages[ind:] :
            if ind+1 < len(self.pages) :
                if j == pg1:
                    ind = self.pages[ind+1:].index(pg1)
                elif j != pg2:
                    counter += 1

                elif j == pg2 : # increment the frequency
                    frequency += 1
                    cum_counter += counter
                    counter = 0 

        return   cum_counter if frequency== 0 else cum_counter/ frequency
      
    def updateLearningRates(self):

        if self.time % (self.seq_len) == 0:
            v = set(self.pages)
            self.row = []
            self.coulmn = []
            for i in range(len(v)):
                for j in range(len(v)):
                    if i==j:
                        self.coulmn.append(0)
                    else:
                         self.coulmn.append(self.page_distances(list(v)[i], list(v)[j]))
                self.row.append(self.coulmn)
                self.column = []

            self.pages = []

            
          

   
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
       
        ###########################
        ## Add frequency table
        
        ##########################
       
        #####################
        ## Visualization data
      

        #####################################################
        ## Adapt learning rate Here
        ###################################################### 
       
        self.pages.append(page)
        self.unique_pages.add(page)
        ref_page = None

        if page not in self.pages_infos:
            #  self.pages_infos[page] = { page+"_dist": self.time,  page+"_freq": 1 }
            self.pages_infos[page]  = page_infos(page, self.time)
            ref_page = self.pages_infos[page]
        else:
            # self.pages_infos[page]= self.pages_infos[page]update(page, self.time)
            ref_page = self.pages_infos[page]
            ref_page.update(page, self.time)

        # print("Target Page:", page)

        for pg in self.pages_infos:
            if pg != page: # update for all the keys other than this  page
                if page in self.pages_infos[pg].frq:
                    self.pages_infos[pg].frq[page] =  self.pages_infos[pg].frq[page] + 1
                    self.pages_infos[pg].dist[page] =  self.pages_infos[pg].dist[page] + (self.time - self.pages_infos[pg].dist[pg])
                else:
                    self.pages_infos[pg].frq[page] =   self.pages_infos[pg].frq[pg]
                    self.pages_infos[pg].frq[page] =   1
                    self.pages_infos[pg].dist[page] =  (self.time - self.pages_infos[pg].dist[pg])
            # print("\t\t")
            # print( "{0:30} {1}".format(" Reference Page", pg) )
            # print("\t\t")
            # print ("{0:30} {1} {2} {3}".format ("Freq:", self.pages_infos[pg].frq[page], " Distance:", self.pages_infos[pg].dist[page]))

        row = []
        rows = []
        for i in self.unique_pages :
            for j in  self.unique_pages :
                if i==j:
                    row.append(0)
                else:
                    if j in self.pages_infos[i].dist:
                        row.append(float(self.pages_infos[i].dist[j]) / self.pages_infos[i].frq[j] )
                        # row.append(self.pages_infos[i].frq[j] )
                    else:
                        row.append(0)
            rows.append(row)
            row = []

        
        model = NMF(n_components=2, init='random', random_state=0)
        W = model.fit_transform(rows)
        H = model.components_
            
        # self.updateLearningRates()


if __name__ == "__main__":
    params = {'cache_size': 3, 'mem_size': 300, }
    alg = nmf(params)
    total_pg_refs = 0
    num_pg_fl = 0

    f = [1,1,2,3,1,3,2,5,1,3,]
   
    for pg in f:
        
        pg_fl = alg.request(pg)
    

    # alg.print_stack()
    # print(total_pg_refs)
    # print(num_pg_fl)
    # print(1.0-num_pg_fl/total_pg_refs)


       



       
            


           
