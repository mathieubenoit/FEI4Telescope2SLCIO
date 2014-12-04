import os, sys

run = int(sys.argv[1])

print "converting Run %06i"%run

os.system("xrdcp root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/pixel-upgrade/itk/BeamTest/cern_2014_october_FEI4tel/cosmic_%06i.root ."%(run))
	
os.system("python /afs/cern.ch/user/m/mbenoit/workspace/Conversion/FEI4Telescope2SLCIO/TelescopeConverter.py cosmic_%06i.root run%06i-converter.slcio %i 8"%(run,run,run))

os.system("xrdcp -f run%06i-converter.slcio root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/pixel-upgrade/itk/BeamTest/cern_2014_october_FEI4tel/lcio/run%06i-converter.slcio"%(run,run))
