# Heavy Stable Charged Particle

## Setup working area

```bash
export SCRAM_ARCH=slc6_amd64_gcc630

cmsrel CMSSW_9_4_3
cd CMSSW_9_4_3/src/
cmsenv

git cms-init
# for the following step you should have a GitHub's ssh key
git clone git@github.com:akalinow/SUSYBSMAnalysis-HSCP.git SUSYBSMAnalysis/HSCP -b Run2_2017

# Before compile, hide BigNTuplizer 
pushd SUSYBSMAnalysis/HSCP/plugins
mv BigNtuplizer.cc BigNtuplizer.cc.bkp
popd

scram b -j8
```

-------------------------------

## Run the code

Steps:

1. Make a first skim from the AOD to some lighter AOD with only the collections needed:

	Directory : `/test/MakeEDMtuples`
	Code: 
	- HSCParticleProducerSingleMu2017_cfg.py and HSCParticleProducerMET2017_cfg.py:  configuration files to run on the SingleMuon and MET datasets, respectively
	- crab_cfg.py crab configuration file

2. test/UsefulScripts/DeDxStudy. Go to the [README](./test/UsefulScripts/DeDxStudy/README.md)

3. test/UsefulScripts/MuonTimingStudy

4. ...

## Run the Step1 on CRAB
Update settings in the CRAB launcher test/AnalysisCode/submitJobs_Launch_1.py. You may want to update:
* localisation of the output files: config.Data.outLFNDirBase
* output storage element: storage_element="T2_PL_Swierk"
* name of the analysis iteration: publish_data_suffix = "HSCP_Run2017_Test5"
* list of files to be run on: datasets. You can run on all samples in Priscilla's direcotry
  listed in datasetsRun2017.py file the exemaple ruin only a single file 
* a single CRAB job runs over all 1000 files in a single 000X directory. This takes about 5h.

```
cd test/AnalysisCode/
./submitJobs_Launch_1.py
```




