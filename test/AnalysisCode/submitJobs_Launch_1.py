#!/usr/bin/env python

import os, re
import commands
import math
import urllib

from crab3 import *
#########################################
#########################################
def prepareCrabCfg(dataset,
                   eventsPerJob,
                   storage_element,
                   publish_data_suffix):

    ###Modyfy runing script to set the correct local path
    aFile = open('run_Analysis_Step1.py')
    contents = aFile.read()
    replaced_contents = contents.replace('DUMMY_PATH', dataset)
    aFile.close()
    aFile = open('run_Analysis_Step1_tmp.py',"w")
    aFile.write(replaced_contents)
    aFile.close()

    ##Modify CRAB3 configuration
    config.JobType.psetName = 'tmpConfig.py'
    config.JobType.disableAutomaticOutputCollection = True
    config.JobType.allowUndistributedCMSSW = True
    config.JobType.scriptExe = 'run_Analysis_Step1_tmp.py'
    config.JobType.outputFiles = ['Histos.root']
    config.JobType.inputFiles = ['FrameworkJobReport.xml']
    config.JobType.inputFiles = ['Analysis_CommonFunction.h', 'Analysis_Global.h', 'Analysis_Samples.h', 'Analysis_Samples_DUMMY.txt', 'Analysis_Step1_EventLoop.C', 'Analysis_PlotFunction.h', 'Analysis_PlotStructure.h', 'Analysis_TOFUtility.h', 'tdrstyle.C']

    shortName = publish_data_suffix
    config.Site.storageSite = storage_element
    config.General.requestName = shortName

    config.Data.outLFNDirBase = '/store/user/akalinow/HSCP/'+publish_data_suffix+"/"
    config.Data.outputDatasetTag = shortName
    config.Data.unitsPerJob = eventsPerJob
    config.Data.totalUnits = 1    
    out = open('crabTmp.py','w')
    out.write(config.pythonise_())
    out.close()
    os.system("crab submit -c crabTmp.py")
#########################################
#########################################
eventsPerJob = 1

#from datasetsRun2017 import datasets

datasets = [
    #SingleMuonB
    "/storage/data/cms/store/user/jpriscia/HSCP_2017/SingleMuon/2017Apr25/180427_073624/0000/"
    ]

for aDataset in datasets:
    prepareCrabCfg(dataset=aDataset,
                   eventsPerJob=eventsPerJob,
                   storage_element="T2_PL_Swierk",
                   publish_data_suffix = "HSCP_Run2017_Test2")                  

