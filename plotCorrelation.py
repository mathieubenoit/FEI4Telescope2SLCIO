from ROOT import TVector3, TLorentzVector, TRandom3, TMath, std, TH1D, TCanvas, TH2D
from JudithData  import *


run  = 3036


inputFolder = "/data/Testbeam_Data/October2014_HVCMOS_FEI4/SPS_October2014"
outputFolder = "/data/Testbeam_Data/October2014_HVCMOS_FEI4/lcio-raw"


corrX = []
corrY = []
corrXY = []

for plane in range(7) : 
	corrX.append(TH2D("plane%iX"%plane,"plane%i"%plane,80,0,80,80,0,80))
	corrY.append(TH2D("plane%iY"%plane,"plane%i"%plane,336,0,336,336,0,336))
	corrXY.append(TH2D("plane%iXY"%plane,"plane%i"%plane,80,0,80,336,0,336))




aDataSet = JudithData("%s/cosmic_%06i/cosmic_%06i.root"%(inputFolder,run,run),7)
MAXEVENTS = aDataSet.GetNEvents()
MAXEVENTS = 10000

refplane = 0


for i in range(MAXEVENTS) : 

	if (i%1000)==0 : 
		print "Event %i"%i
        telescopeData=aDataSet.GetEvent(i)

	for i,plot in enumerate(corrX) : 
		for hitx in telescopeData[refplane]:
			for hity in telescopeData[i]:	
				plot.Fill(hitx[0],hity[0])
				
	for i,plot in enumerate(corrY) : 
		for hitx in telescopeData[refplane]:
			for hity in telescopeData[i]:	
				plot.Fill(hitx[1],hity[1])
	
	for i,plot in enumerate(corrXY) : 
		for hitx in telescopeData[refplane]:
			for hity in telescopeData[i]:	
				plot.Fill(hitx[0],hity[1])



cans = []
for i,plot in enumerate(corrX) :
	cans.append(TCanvas())
	plot.Draw("colz")

for i,plot in enumerate(corrY) :
	cans.append(TCanvas())
	plot.Draw("colz")

for i,plot in enumerate(corrXY) :
	cans.append(TCanvas())
	plot.Draw("colz")
