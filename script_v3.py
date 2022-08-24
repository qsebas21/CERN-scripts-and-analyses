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
    
    
    #create two dictionaries of daughters of Lcstar and Lc: one with PIDs (to reconstruct the decay) and one with MCParticle objects
    pid_dict = dict()
    parts_dict = dict()

    for i in parts:
        i_index = i.index()
        pid = i.particleID().pid()
        if abs(pid) == 4214 or abs(pid) == 4122:
            daughters_pid = set()
            daughters_parts = set()
            
            for j in parts:
                try:
                    if j.mother().index() == i_index:
                        daughters_pid.add(j.particleID().pid())
                        daughters_parts.add(j)
                except:
                    continue
                if len(daughters_pid) == 3:
                    break
                    
            #pid_dict.sort()    #for alternative part down below
            pid_dict[i_index] = daughters_pid
            parts_dict[i_index] = daughters_parts
            
       
    #check if this event has a complete decay 
    has_dec = False
    try:
        if 4122 in pid_dict[4214] and -211 in pid_dict[4214] and 211 in pid_dict[4214] and 2212 in pid_dict[4122] and 211 in pid_dict[4122] and -321 in pid_dict[4122]:
            has_dec = True
    except:
        try:
            if -4122 in pid_dict[-4214] and 211 in pid_dict[-4214] and 211 in pid_dict[-4214] and -2212 in pid_dict[-4122] and -211 in pid_dict[-4122] and 321 in pid_dict[-4122]: 
                has_dec = True
        except:
            continue
            
    #alternatively,
#    
#    try:
#        if (pid_dict[4214] == [-211,211,4122] and pid_dict[4122] == [-321,211,2212]) or (pid_dict[-4214] == [-4122,-211,211] and pid_dict[-4122] == [-2212,-211,321])
#    except:
#        continue    
        
    if has_dec is False:
        continue    
    
    
    #create sets of particles (that we care about: Lcstar, Lc (unlikely to hit but added for completeness), p, K, pi) which hit VP/UT/MS 
    good_pids = [211,321,2212,4122,4214]
    vp_parts = set()
    for i in vp_hits:
        i_pid = i.mcParticle().particleID().pid()
        if abs(i_pid) in good_pids:
            vp_parts.add(i.mcParticle())

    ut_parts = set()
    for i in ut_hits:
        i_pid = i.mcParticle().particleID().pid()
        if abs(i_pid) in good_pids:
            ut_parts.add(i.mcParticle())
                    
    ms_parts = set()
    for i in ms_hits:
        i_pid = i.mcParticle().particleID().pid()
        if abs(i_pid) in good_pids:
            ms_parts.add(i.mcParticle())        
    
    #check if daughters were detected by VP/UT/MS
    
    try:
        if (parts_dict[4214][0] in vp_parts or parts_dict[4214][1] in vp_parts or parts_dict[4214][2] in vp_parts) and parts_dict[4122][0] in vp_parts and parts_dict[4122][1] in vp_parts and parts_dict[4122][2] in vp_parts:
            vp_decs += 1
    except:
        if (parts_dict[-4214][0] in vp_parts or parts_dict[-4214][1] in vp_parts or parts_dict[-4214][2] in vp_parts) and parts_dict[-4122][0] in vp_parts and parts_dict[-4122][1] in vp_parts and parts_dict[-4122][2] in vp_parts:
                vp_decs += 1
            
    try:
        if (parts_dict[4214][0] in ut_parts or parts_dict[4214][1] in ut_parts or parts_dict[4214][2] in ut_parts) and parts_dict[4122][0] in ut_parts and parts_dict[4122][1] in ut_parts and parts_dict[4122][2] in ut_parts:
            ut_decs += 1
    except:
        if (parts_dict[-4214][0] in ut_parts or parts_dict[-4214][1] in ut_parts and parts_dict[-4214][2] in ut_parts) and parts_dict[-4122][0] in ut_parts and parts_dict[-4122][1] in ut_parts and parts_dict[-4122][2] in ut_parts:
                ut_decs += 1
    
    try:
        if (parts_dict[4214][0] in ms_parts or parts_dict[4214][1] in ms_parts or parts_dict[4214][2] in ms_parts) and (parts_dict[4122][0] in ms_parts or parts_dict[4122][1] in ms_parts or parts_dict[4122][2] in ms_parts):
            ms_decs += 1
    except:
        if (parts_dict[-4214][0] in ms_parts or parts_dict[-4214][1] in ms_parts or parts_dict[-4214][2] in ms_parts) and (parts_dict[-4122][0] in ms_parts or parts_dict[-4122][1] in ms_parts or parts_dict[-4122][2] in ms_parts):
                ms_decs += 1
                    
with open("output.txt", "w") as f:
    print('There are ' + str(vp_decs) + ' decays in VP.', file=f)
    print('There are ' + str(ut_decs) + ' decays in UT.', file=f)
    print('There are ' + str(ms_decs) + ' decays in MS.', file=f)

    if vp_decs + ut_decs == 0:
        print('No decays in VP + UT.', file=f)
    else:
        print('The total gain is ' + str(1 + ms_decs/(vp_decs + ut_decs)), file=f)

