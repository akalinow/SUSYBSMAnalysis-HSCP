#!/usr/bin/env python
####################################
#        LaunchOnFarm Script       #
#     Loic.quertenmont@cern.ch     #
#            April 2010            #
#  Artur.Kalinowski@fuw.edu.pl     #
#           December 2019          #
####################################

import os
import os.path
import commands

os.system("pwd")
os.system("ls -ltr")
os.system("ls -ltr /srv/CMSSW_9_4_3/src/SUSYBSMAnalysis/HSCP/data")
os.system("ls -ltr /srv/CMSSW_9_4_3/src/SUSYBSMAnalysis/HSCP/test/AnalysisCode/../../")
os.system("ls -ltr /srv/CMSSW_9_4_3/src/SUSYBSMAnalysis/HSCP/test/AnalysisCode/../../data/")

#localPath = "/home/akalinow/scratch/CMS/HSCP/Data/HSCP_2017/SingleMuon/2017Apr25/180426_092321/0000/"
localPath = "DUMMY_PATH"
fileList = os.listdir(localPath)

fileNamesString = ""
for fileName in fileList:
    if fileName.find(".root")>0:
        fileName = fileName.rstrip(".root")
        fileNamesString += fileName+";"

fileNamesString = fileNamesString.rstrip(";")

print("Number of files to process:",len(fileNamesString.split(";")))
aFile = open('Analysis_Samples_DUMMY.txt')
contents = aFile.read()
replaced_contents = contents.replace('DUMMY', fileNamesString)
aFile.close()
aFile = open('Analysis_Samples.txt',"w")
aFile.write(replaced_contents)
aFile.close()

import ROOT
from DataFormats.FWLite import Events, Handle

makeshared = ROOT.TString(ROOT.gSystem.GetMakeSharedLib())
makeshared.ReplaceAll("-W ", "-Wno-deprecated-declarations -Wno-deprecated -Wno-unused-local-typedefs -Wno-attributes ")
makeshared.ReplaceAll("-Woverloaded-virtual ", " ")
makeshared.ReplaceAll("-Wshadow ", " -std=c++0x -D__USE_XOPEN2K8 ")
print("Compilling with the following arguments:",makeshared)
ROOT.gSystem.SetMakeSharedLib(makeshared.Data())
ROOT.gSystem.SetIncludePath("-I$ROOFITSYS/include")
ROOT.gInterpreter.SetClassAutoparsing(False)
ROOT.FWLiteEnabler.enable()
ROOT.gSystem.CompileMacro('Analysis_Step1_EventLoop.C')

from ROOT import Analysis_Step1_EventLoop
Analysis_Step1_EventLoop(localPath, 0,  "Data13TeV16")


#Run dummy CMSSW configuration to produce the framework report
cmsRun -j FrameworkJobReport.xml -p PSet.py
