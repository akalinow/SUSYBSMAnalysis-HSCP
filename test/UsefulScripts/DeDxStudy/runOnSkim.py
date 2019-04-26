#!/usr/bin/env python

import urllib
import string
import os,sys,time
import SUSYBSMAnalysis.HSCP.LaunchOnCondor as LaunchOnCondor  
import glob
import commands
import json
import collections # kind of map
from pdb import set_trace



def getChunksFromList(MyList, n):
  return [MyList[x:x+n] for x in range(0, len(MyList), n)]

def initProxy():
   if(not os.path.isfile(os.path.expanduser('~/private/x509_proxy')) or ((time.time() - os.path.getmtime(os.path.expanduser('~/private/x509_proxy')))>600)):
      print "You are going to run on a sample over grid using either CRAB or the AAA protocol, it is therefore needed to initialize your grid certificate"
      os.system('mkdir -p ~/x509_user_proxy; voms-proxy-init --voms cms -valid 192:00 --out ~/private/x509_proxy')#all must be done in the same command to avoid environement problems.  Note that the first sourcing is only needed in Louvain


if len(sys.argv)==1:
        print "Please pass in argument a number between 1 and 3"
        print "  1  - Run dEdxStudy on RECO, AOD, or dEdxSKIM files         --> submitting 1job per file"
        print "  2  - Hadd root files containing the histograms             --> interactive processing" 
        print "  3  - run the plotter on the hadded root files              --> interactive processing" 
        sys.exit()



datasetList = [
#  ["Run278018", "/storage/data/cms/store/user/jozobec/dEdxCalib/278018/","listFiles_278018.txt"],
#  ["Run278308", "/storage/data/cms/store/user/jozobec/dEdxCalib/278308/","listFiles_278308.txt"],
#  ["Run279931", "/storage/data/cms/store/user/jozobec/dEdxCalib/279931/","listFiles_279931.txt"],
#  ["RunPostG", "/eos/user/j/jpriscia/out/postG/"]
  ["Region2",  "/eos/user/j/jpriscia/out/Region2/"],
  ["Region3",  "/eos/user/j/jpriscia/out/Region3/"],
  ["Region4",  "/eos/user/j/jpriscia/out/Region4/"],
#  ["RunPreG", "/eos/user/j/jpriscia/out/preG/"],
#  ["Run278018", "/eos/user/j/jpriscia/out/278018/"],
#  ["Run278308", "/eos/user/j/jpriscia/out/278308/"],
#  ["Run279931", "/eos/user/j/jpriscia/out/279931/"],
##  ["Run280385", "/storage/data/cms/store/user/jozobec/dEdxCalib/280385/"],

#  ["MCGluino_M1000_f10", "Gluino_13TeV_M1000_f10"],
#  ["MCGluino_M1400_f10", "Gluino_13TeV_M1400_f10"],
#  ["MCGluino_M1800_f10", "Gluino_13TeV_M1800_f10"],
#  ["MCGluino_M1000_f50", "Gluino_13TeV_M1000_f50"],
#  ["MCGluino_M1400_f50", "Gluino_13TeV_M1400_f50"],
#  ["MCGluino_M1800_f50", "Gluino_13TeV_M1800_f50"],
#  ["MCGMStau_M494",      "GMStau_13TeV_M494"],
#  ["MCStop_M1000",       "Stop_13TeV_M1000"],
#  ["MCDYM2600Q2",        "DY_13TeV_M2600_Q2"],
]

isLocal = True  #allow to access data in Louvain from remote sites
#if(commands.getstatusoutput("hostname -f")[1].find("ucl.ac.be")!=-1): isLocal = True
#os.system('rm -rf ~/x509_user_proxy/x509_proxy')


if sys.argv[1]=='1':
        os.system("sh " + os.getcwd() + "/DeDxStudy.sh ") #just compile

	for DATASET in datasetList :
	   outdir =  os.getcwd() + "/Histos/"+DATASET[0]+"/"
	   os.system('mkdir -p ' + outdir)

	   JobName = "DEDXHISTO_"+DATASET[0]
	   FarmDirectory = "FARM_DEDXHISTO_"+DATASET[0]
           LaunchOnCondor.subTool = 'condor'
	   LaunchOnCondor.SendCluster_Create(FarmDirectory, JobName)

 	   FILELIST = []        
           if(DATASET[1][-1]=='/'): #file path is a directory, consider all files from the directory
              if(isLocal):
      	         FILELIST = LaunchOnCondor.GetListOfFiles('', DATASET[1]+'/*.root', '')
              else:
                 initProxy()
                 initCommand = 'export X509_USER_PROXY=~/private/x509_proxy; voms-proxy-init --noregen;'
                 LaunchOnCondor.Jobs_InitCmds = [initCommand]
                 #print initCommand+'lcg-ls -b -D srmv2 "srm://ingrid-se02.cism.ucl.ac.be:8444/srm/managerv2?SFN='+DATASET[1]+'" | xargs -I {} basename {}'
                 #print commands.getstatusoutput(initCommand+'lcg-ls -b -D srmv2 "srm://ingrid-se02.cism.ucl.ac.be:8444/srm/managerv2?SFN='+DATASET[1]+'" | xargs -I {} basename {}')
                 #LocalFileList = commands.getstatusoutput(initCommand+'lcg-ls -b -D srmv2 "srm://ingrid-se02.cism.ucl.ac.be:8444/srm/managerv2?SFN='+DATASET[1]+'" | xargs -I {} basename {}')[1].split('\n')

                 with open(DATASET[2], 'r') as fileList:
                   for f in fileList:
                     #if(f[-5:].find('.root')==-1):continue #only .root file considered
                     FILELIST += ["root://cms-xrd-global.cern.ch/"+DATASET[1].replace('/storage/data/cms/store/','/store/')+f.rstrip()]
    
           else: #file path is an HSCP sample name, use the name to run the job
             FILELIST += [DATASET[1]]
             

           print FILELIST
           for inFileList in getChunksFromList(FILELIST,max(1,len(FILELIST)/50)): #50 jobs, this is a trade off between hadding time and processing time
              InputListCSV = ''
  	      for inFile in inFileList:
                 InputListCSV+= inFile + ','
              InputListCSV = InputListCSV[:-1] #remove the last duplicated comma
              LaunchOnCondor.SendCluster_Push  (["BASH", "sh " + os.getcwd() + "/DeDxStudy.sh " + InputListCSV + " out.root; mv out.root " + outdir+"dEdxHistos_%i.root" %  LaunchOnCondor.Jobs_Count ])
	   LaunchOnCondor.SendCluster_Submit()

elif sys.argv[1]=='2':
        for DATASET in datasetList :#+signalList :
           indir =  os.getcwd() + "/Histos/"+DATASET[0]+'/'
           os.system('rm -f Histos_'+DATASET[0]+'.root')
           os.system('find ' + indir + '*.root  -type f -size +1024c | xargs hadd -f Histos_'+DATASET[0]+'.root')
	# finally merge all the runs into the histogram with data
	#os.system('rm -f Histos_Data.root')
	#os.system('hadd -f Histos_Data.root Histos_Run*.root')

elif sys.argv[1]=='3':
        os.system('sh MakePlot.sh')

else:
   print "Invalid argument"
   sys.exit()

