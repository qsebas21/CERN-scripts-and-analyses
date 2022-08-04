import GaudiPython as GP
from GaudiConf import IOHelper
from Configurables import CondDB, LHCbApp, EventSelector, Gaudi__RootCnvSvc, ApplicationMgr, EventDataSvc, EventPersistencySvc, MessageSvc


appConf = ApplicationMgr()
appConf.ExtSvc.append('Gaudi::IODataManager/IODataManager')
appConf.ExtSvc.append('Gaudi::RootCnvSvc/RootCnvSvc')
EventDataSvc().RootCLID         = 1
EventDataSvc().EnableFaultHandler = True
root = Gaudi__RootCnvSvc('RootCnvSvc')
root.CacheBranches = ['/Event/MC/*']
root.VetoBranches = []
EventPersistencySvc().CnvServices.append(root)
EventSelector().Input = ["DATA='PFN:/afs/cern.ch/work/j/jmalczew/public/Lcstar2Lcpipi_101ev_noPacking.sim' SVC='Gaudi::RootEvtSelector'"]
EventSelector().PrintFreq = 1
MessageSvc().OutputLevel = 3

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()

import numpy as np

simulated = 101

#evts_with_both = 0
 
for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']



    #create a dictionary with the daughters of Lc_star only
    daughtersLc = dict()

    for i in parts:
        if abs(i.particleID().pid()) == 4214 or abs(i.particleID().pid() == 4122):
            daughters = list()
            for j in parts:
                try:
                    if j.mother().index() == i.index():
                        daughters.append(j)
                except:
                    continue
            daughtersLc[i.index()] = daughters
