from ROOT import * 



class JudithData:
    """A container for TBTrack Data """

    RunNumber = 0

    judith_file = 0

    planeTrees = []
    

    HitInCluster = []
    NHits = []
    PixX = []
    PixY = []
    Lv1 = []
    ToT = []
    
    
    
    def __init__(self,rootfile_name,nplanes) :
        
        self.judith_file = TFile(rootfile_name,"open")
 
        for plane in range(nplanes):       
            self.HitInCluster.append(0)
            self.NHits.append(0)
            self.PixX.append(0)
            self.PixY.append(0)
            self.Lv1.append(0)
            self.ToT .append(0)   
        
        for plane in range(nplanes):            
            self.planeTrees.append(self.judith_file.Get("Plane%i/Hits"%plane))

  
        for plane in range(nplanes):            
            self.HitInCluster[plane]   = self.planeTrees[plane].HitInCluster
            self.NHits[plane]           = self.planeTrees[plane].NHits
            self.PixX[plane]            = self.planeTrees[plane].PixX
            self.PixY[plane]            = self.planeTrees[plane].PixY
            self.Lv1[plane]             = self.planeTrees[plane].Timing
            self.ToT [plane]            = self.planeTrees[plane].Value
                    
    
    def GetEvent(self,event_nr):
        
        for tree in  self.planeTrees : 
            tree.GetEntry(event_nr)
	    
        for plane in range(7):            
            self.HitInCluster[plane]   = self.planeTrees[plane].HitInCluster
            self.NHits[plane]           = self.planeTrees[plane].NHits
            self.PixX[plane]            = self.planeTrees[plane].PixX
            self.PixY[plane]            = self.planeTrees[plane].PixY
            self.Lv1[plane]             = self.planeTrees[plane].Timing
            self.ToT [plane]            = self.planeTrees[plane].Value	       
        
        telescopeData = [[] for i in range(len(self.planeTrees))]
        
	for i in range(len(self.planeTrees)) :
            for j,tot in enumerate(self.ToT) : 
                
                try :
			if((self.PixX[i][j]!=0 and self.PixY[i][j]!=0)) :
                	    if((self.PixX[i][j]>=0 and self.PixY[i][j]>=0) and (self.PixX[i][j]<80 and self.PixY[i][j]<=336)) :
                        	telescopeData[i].append([self.PixX[i][j],self.PixY[i][j],self.ToT[i][j],self.Lv1[i][j]])
            	except : 
			pass
            
        return telescopeData
        

        
    def GetNEvents(self):
        return self.planeTrees[0].GetEntries()
        
    
    
    def PrintEvent(self,eventnr):
        print "-----------------------------------------"
        telescopeData=self.GetEvent(eventnr)
        
        print "Event #%i"%eventnr
        for i in range(len(telescopeData)):
            
            print "Plane %i"%i
            
            for hit in telescopeData[i] : 
                print "X:%i Y:%i TOT:%i LV1:%i"%(hit[0],hit[1],hit[2],hit[3])
            


# aDataSet = JudithData("/data/Testbeam_Data/August2014_HVCMOS_FEI4/RunData/cosmic_C19_2207-2222.root",7)
# 
# 
# for i in range(1000) : 
# 
#     aDataSet.PrintEvent(i)





















