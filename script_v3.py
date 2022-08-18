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
EventSelector().Input = ["DATA='PFN:/afs/cern.ch/work/j/jmalczew/public/Lcstar2Lcpipi_1000ev_noPacking_UTandLcFixed.sim' SVC='Gaudi::RootEvtSelector'"]
EventSelector().PrintFreq = 1
MessageSvc().OutputLevel = 3

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()

simulated = 1000

vp_decs = 0
ut_decs = 0
ms_decs = 0


for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    vp_hits = evt['/Event/MC/VP/Hits']
    ms_hits = evt['/Event/MC/MS/Hits']
    ut_hits = evt['/Event/MC/UT/Hits']
    
    unique_Lcstar = list()    
    daughtersLc = dict()
    
    for i in parts:
        pid = i.particleID().pid()
        i_index = i.index()
        
        if i_index not in unique_Lcstar and (abs(pid) == 4214 or abs(pid) == 4122):
            unique_Lc.append(i_index)
            daughters = set()
            
            for j in vp_hits:
                try:
                    if j.mcParticle().mother().index() == i_index:
                        daughters.add(j.mcParticle().particleID().pid())
                except:
                    continue
                
                if len(daughters) == 3:
                    break
                    
            if 2212 in daughters and 211 in daughters and 321 in daughters:
                vp_decs += 1
                
            daughters = set()
            
            for k in ut_hits:
                try:
                    if j.mcParticle().mother().index() == i_index:
                        daughters.add(abs(j.mcParticle().particleID().pid()))
                except:
                    continue
                
                if len(daughters) == 3:
                    break
                    
            if 2212 in daughters and 211 in daughters and 321 in daughters:
                ut_decs += 1
                
            daughters = set()
            
            for l in ms_hits:
                try:
                    if j.mcParticle().mother().index() == i_index:
                        daughters.add(abs(j.mcParticle().particleID().pid()))
                except:
                    continue
                
                if len(daughters) == 3:
                    break
                    
            if 2212 in daughters or 211 in daughters or 321 in daughters:
                ms_decs += 1
                
print('There are ' + str(vp_decs) + ' decays in VP.')
print('There are ' + str(ut_decs) + ' decays in UT.')
print('There are ' + str(ms_decs) + ' decays in MS.')

if vp_decs + ut_decs == 0:
    print('No decays in VP + UT.')
else:
    print('The total gain is ' + str(1 + ms_decs/(vp_decs + ut_decs)))
