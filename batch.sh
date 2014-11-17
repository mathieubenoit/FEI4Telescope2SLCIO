#!/bin/bash

#BSUB -J CalibTree[2758-3011]
#BSUB -q 8nh
#BSUB -o /afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_CuXRF/jobs/out.%J_%I
#BSUB -e /afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_CuXRF/jobs/err.%J_%I
#BSUB -R "type==SLC6_64"

#for LSB_JOBINDEX in {2758..3011}
#do
RUNID=$(( $LSB_JOBINDEX ))
#echo $XMIN
#done


source /home/mbenoit/workspace/FEI4Telescope2SLCIO/setup_pyLCIO.sh


python Convert.py $RUNID
