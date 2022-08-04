import sys
sys.path
import GaudiPython as GP

from Configurables import EventSelector, Gaudi__RootCnvSvc, ApplicationMgr, EventDataSvc, EventPersistencySvc, MessageSvc

import pandas as pd
import numpy as np

from ROOT import TH1D

appConf = ApplicationMgr()
appConf.ExtSvc.append('Gaudi::IODataManager/IODataManager')
appConf.ExtSvc.append('Gaudi::RootCnvSvc/RootCnvSvc')
EventDataSvc().RootCLID         = 1
EventDataSvc().EnableFaultHandler = True
root = Gaudi__RootCnvSvc('RootCnvSvc')
root.CacheBranches = ['/Event/MC/*']
root.VetoBranches = []
EventPersistencySvc().CnvServices.append(root)
EventSelector().Input = ["DATA='PFN:/Tuple_noPacking.sim' SVC='Gaudi::RootEvtSelector'"]

EventSelector().PrintFreq = 1
MessageSvc().OutputLevel = 3

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()
