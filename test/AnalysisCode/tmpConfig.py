import FWCore.ParameterSet.Config as cms

process = cms.Process("DUMMY")

process.source = cms.Source("EmptySource",
                            firstRun = cms.untracked.uint32(1),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1))
process.schedule = cms.Schedule()
