from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = ''
config.General.workArea = 'v1'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'PSet.py'
config.JobType.sendExternalFolder = True

config.section_("Data")
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 2000 #number of files per jobs
config.Data.totalUnits =  -1 #number of event
config.Data.outLFNDirBase = '/store/user/akalinow/'
config.Data.publication = False
config.Data.outputDatasetTag = ''

config.section_("Site")
config.Site.storageSite = 'T2_PL_Swierk'
config.Site.whitelist = ['T2_BE_UCL']
