'''
Created on June 17, 2013

Tool to convert allpix telescope simulation files into LCIO EUTelescope format.

@author: <a href="mailto:samir.arfaoui@cern.ch">Samir Arfaoui</a>
'''

from pyLCIO import  UTIL
from ROOT import TVector3, TLorentzVector, TRandom3, TMath, std, TH1D, TCanvas, TH2D
from JudithData  import *
from math import floor

#Compiled with Cython if available, comment otherwise
#import pyximport; pyximport.install(pyimport=True)

from pyLCIO import EVENT,IMPL,IOIMPL
from time import time
import sys, math, glob, tarfile
from collections import defaultdict

telescopeTestDict = {}
telescopeTestDict['300'] = 0
telescopeTestDict['301'] = 0
telescopeTestDict['302'] = 0
telescopeTestDict['303'] = 0
telescopeTestDict['304'] = 0
telescopeTestDict['305'] = 0

print sys.argv[3:]

mySensorIDlist = sys.argv[3:]
for mySensorID in mySensorIDlist:
    telescopeTestDict[mySensorID] = 0





#########################################################################################
def convertRun( inputFileName, outputFileName, runNumber, nplanes=7 ):
    

    # define detector name
    detectorName = 'FEI4Tel'

    # create a writer and open the output file
    writer = IOIMPL.LCFactory.getInstance().createLCWriter()
    writer.open( outputFileName, EVENT.LCIO.WRITE_NEW )

    # create a run header and add it to the file
    run = IMPL.LCRunHeaderImpl()
    run.setRunNumber( runNumber )
    run.setDetectorName( detectorName )
    run.parameters().setValue  ( 'GeoID'            , 0 )
    run.parameters().setValues ( 'MaxX'             , std.vector(int)(nplanes,335) ) 
    run.parameters().setValues ( 'MaxY'             , std.vector(int)(nplanes,79) )
    run.parameters().setValues ( 'MinX'             , std.vector(int)(nplanes,0) ) 
    run.parameters().setValues ( 'MinY'             , std.vector(int)(nplanes,0) )
    run.parameters().setValue  ( 'NoOfDetector'     , nplanes )
    run.parameters().setValues ( 'AppliedProcessor' , std.vector('string')(1,'') )
    run.parameters().setValue  ( 'DAQHWName'        , 'EUDRB' )
    run.parameters().setValue  ( 'DAQSWName'        , 'EUDAQ' )
    run.parameters().setValue  ( 'DataType'         , 'Data' )
    run.parameters().setValue  ( 'DateTime'         , '24.12.2000  23:59:59.000000000' )
    run.parameters().setValue  ( 'EUDRBDet'         , 'MIMOSA26' )
    run.parameters().setValue  ( 'EUDRBMode'        , 'ZS2' )
    writer.writeRunHeader( run )
  

    aDataSet = JudithData(inputFileName,nplanes)

    MAXEVENTS = aDataSet.GetNEvents()
    #MAXEVENTS = 500
 
    NEVENTS   = 0

    # event loop
    
    for eventnr in range(MAXEVENTS):

        if ( eventnr%1000 == 0 ):
            print 'Events processed: %i ...' % eventnr

        # create an event and set its parameters
        event = IMPL.LCEventImpl()
        event.setEventNumber( eventnr )
        event.setDetectorName( detectorName )
        event.setRunNumber( runNumber )
        event.setTimeStamp( int( time() * 1000000000. ) )
        event.parameters().setValue( 'EventType', 2 )

        # parse input file
        telescopeData=aDataSet.GetEvent(eventnr)
	#aDataSet.PrintEvent(eventnr)

        # if first event, create additional setup collection(s)
        if eventnr == 0:
            
            eudrbSetup = IMPL.LCCollectionVec( EVENT.LCIO.LCGENERICOBJECT )
            
            # collection parameters
            eudrbSetup.parameters().setValue( 'DataDescription', 'type:i,mode:i,spare1:i,spare2:i,spare3:i' )
            eudrbSetup.parameters().setValue( 'TypeName', 'Setup Description' )
            
            # create on setup object per Telescope plane
            for sensorID in range(nplanes):
                                    
                setupObj = IMPL.LCGenericObjectImpl(5,0,0)
                setupObj.setIntVal( 0, 102 )
                setupObj.setIntVal( 1, 101 )     
                eudrbSetup.addElement( setupObj )

            event.addCollection ( eudrbSetup, 'eudrbSetup' )


        # ID encoder info
        encodingString = 'sensorID:5,sparsePixelType:5'

        # Telescope data collection
        trackerDataColl = IMPL.LCCollectionVec( EVENT.LCIO.TRACKERDATA )
        idEncoder_Telescope = UTIL.CellIDEncoder( IMPL.TrackerDataImpl )( encodingString, trackerDataColl )


        # fill telescope collection
        for sensorID in range(nplanes):
            
            planeData = IMPL.TrackerDataImpl()

            idEncoder_Telescope.reset()
            
	    plane_tmp =0
	    if(sensorID==0) :
	    	idEncoder_Telescope['sensorID'] = int( 6 ) # cannot fit 300 in 5 bits!! FIXME
	    	plane_tmp =6

            else :
	    	idEncoder_Telescope['sensorID'] = int( sensorID-1 ) # cannot fit 300 in 5 bits!! FIXME
	    	plane_tmp =int( sensorID-1 )

	    
	    idEncoder_Telescope['sparsePixelType'] = 2
            idEncoder_Telescope.setCellID( planeData )
            
            # loop over hits
            chargeVec = std.vector(float)()
            for hit in telescopeData[sensorID]:
		for j,val in enumerate(hit) :
						
		    if ((plane_tmp==6) and (j%4)==1 ) :		    	
			chargeVec.push_back( int(floor(val/2.0)) )
		    else : 
			chargeVec.push_back( val )
			 
			
            planeData.setChargeValues( chargeVec )

            trackerDataColl.addElement( planeData )

        event.addCollection( trackerDataColl, 'zsdata_FEI4' )

        writer.writeEvent( event )
    
    writer.flush()
    writer.close()
    











#########################################################################################
def usage():
    print 'Converts allpix generated telescope files into LCIO format'
    print 'Usage:\n python %s <inputRootFile> <outputFile> runnumber nplanes' % ( sys.argv[0] )

#########################################################################################





if __name__ == '__main__':
    if len( sys.argv ) < 3:
        usage()
        sys.exit( 1 )
    convertRun( sys.argv[1], sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))

    for sensorID in sorted( telescopeTestDict.iterkeys() ):
        print sensorID, telescopeTestDict[sensorID]
