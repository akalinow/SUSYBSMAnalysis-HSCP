import FWCore.ParameterSet.Config as cms

process = cms.Process("DUMMY")

process.source = cms.Source("EmptySource",
    firstRun = cms.untracked.uint32(31)
)

process.schedule = cms.Schedule()
