import os, sys

run = int(sys.argv[1])

os.system("xrdcp -R root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/pixel-upgrade/itk/BeamTest/cern_2014_october_FEI4tel/cosmic_%06i/ cosmic_%06i/"%(run,run))
	
os.system("python TelescopeConverter.py cosmic_%06i/cosmic_%06i.root run%06i-converter.slcio %i 7"%(run,run,run,run))

os.system("xrdcp run%06i-converter.slcio root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/pixel-upgrade/itk/BeamTest/cern_2014_october_FEI4tel/lcio/run%06i-converter.slcio"%(run,run))
