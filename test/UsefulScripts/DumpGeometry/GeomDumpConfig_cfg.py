import FWCore.ParameterSet.Config as cms

process = cms.Process("GeometryDump")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.Services_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v32', '')

process.options   = cms.untracked.PSet(
      wantSummary = cms.untracked.bool(True),
      SkipEvent = cms.untracked.vstring('ProductNotFound'),
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.TFileService = cms.Service("TFileService",  
          fileName = cms.string('CMS_GeomTree.root') 
) 

process.source = cms.Source("EmptyIOVSource", #LQ: I guess the alignement may depend on the run number
    timetype   = cms.string('runnumber'),
    interval   = cms.uint64(1),
    firstValue = cms.uint64(251252),
    lastValue  = cms.uint64(251253)
)


process.GeomDumper = cms.EDAnalyzer("GeomDumpForFWLite") 
process.DumpPath = cms.Path(process.GeomDumper)
process.schedule = cms.Schedule(process.DumpPath)
