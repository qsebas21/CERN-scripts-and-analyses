import sys
sys.path

import sys
import GaudiPython as GP
from GaudiConf import IOHelper
from Configurables import EventSelector, Gaudi__RootCnvSvc, ApplicationMgr, EventDataSvc, EventPersistencySvc, MessageSvc #CondDB, LHCbApp, 
#from Configurables import DataPacking__Unpack_LHCb__MCMSHitPacker_ as MCMSHitUnpacker
#from Configurables import DataPacking__Unpack_LHCb__MCFTHitPacker_ as MCFTHitUnpacker
#from Configurables import UnpackMCParticle
#from Configurables import UnpackMCVertex
import pandas as pd
import numpy as np

from ROOT import TH1D

appConf = ApplicationMgr()
#appConf.HistogramPersistency = 'NONE'
appConf.ExtSvc.append('Gaudi::IODataManager/IODataManager')
appConf.ExtSvc.append('Gaudi::RootCnvSvc/RootCnvSvc')
#unpacker0 = UnpackMCVertex('UnpackMCVertices')
#unpacker0.RootInTES = '/Event'
#unpacker1 = MCMSHitUnpacker('UnpackMCMSHits')
#unpacker1.RootInTES = '/Event'
#unpacker2 = UnpackMCParticle('UnpackMCParticles')
#unpacker2.RootInTES = '/Event'
#unpacker3 = MCFTHitUnpacker('UnpackMCFTHits')
#unpacker3.RootInTES = '/Event'
#appConf.TopAlg.append(unpacker0)
#appConf.TopAlg.append(unpacker1)
#appConf.TopAlg.append(unpacker2)
#appConf.TopAlg.append(unpacker3)
EventDataSvc().RootCLID         = 1
EventDataSvc().EnableFaultHandler = True
root = Gaudi__RootCnvSvc('RootCnvSvc')
root.CacheBranches = ['/Event/MC/*']
root.VetoBranches = []
EventPersistencySvc().CnvServices.append(root)
EventSelector().Input = [
#        "DATA='PFN:../MagnetStations_Lc2625_PGun.sim' SVC='Gaudi::RootEvtSelector'",
    "DATA='PFN:/Tuple_noPacking.sim' SVC='Gaudi::RootEvtSelector'", #what is PFN?
#        "DATA='PFN:../run_pgun_2/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
#        "DATA='PFN:../run_pgun_3/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
#        "DATA='PFN:../run_pgun_4/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
#        "DATA='PFN:../run_pgun_5/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
#        "DATA='PFN:../run_pgun_6/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
#        "DATA='PFN:../run_pgun_7/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
#        "DATA='PFN:../run_pgun_8/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
#        "DATA='PFN:../run_pgun_9/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
#        "DATA='PFN:../run_pgun_10/MagnetStations_PGun.sim' SVC='Gaudi::RootEvtSelector'",
        ]
EventSelector().PrintFreq = 1
MessageSvc().OutputLevel = 3

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()

import numpy as np

all_dfs = []
all_dfs_signal = []

nDstar=0
simulated=50000


f=TFile( #what does this do?



pi_in_general=0

for i in range(simulated):
    appMgr.run(1)
    hits = evt['/Event/MC/Hits']
    ms_hits = evt['/Event/MC/MS/Hits']
    vp_hits = evt['/Event/MC/VP/Hits']
    #phits_ft = evt['/Event/pSim/FT/Hits']
    #phits_tt = evt['/Event/MC/UT/Hits']
    mcparts = evt['/Event/MC/Particles']
    records = []
    records_signal = []

    #print hits.data().size()
    print ms_hits.data().size()
    print vp_hits.data().size()
    #print phits_ft.data().size()
    #print phits_tt.data().size()

    print i

    try:
        hit_mcpids = set()
        #hit_mcpids_ft = set()
        #hit_mcpids_tt = set()
        hit_mcpids_vp = set()

        #phits_ft_data = phits_ft.data()
        #phits_tt_data = phits_tt.data()
        phits_vp_data = phits_vp.data()



        for j in range(len(phits_ft_data)):
            mcpid = phits_ft_data[j].mcParticle
            hit_mcpids_ft.add(mcpid)
        for j in range(len(phits_tt_data)):
            mcpid = phits_tt_data[j].mcParticle
            hit_mcpids_tt.add(mcpid)
        for j in range(len(phits_vp_data)):
            mcpid = phits_vp_data[j].mcParticle
            hit_mcpids_vp.add(mcpid)

        print 'event', i, 'len= ', phits.data().size()

        for j in range(len(hits)):
            # Array index of MC particle that caused this hit
            mcpid = phits.data()[j].mcParticle
            # Get the MC particle
            part = mcparts[mcpid]

            
            

            hit_mcpids.add(mcpid)

            if abs(part.momentum().Z()) < 1e-30:
                tx = -10000
            else:
                tx = part.momentum().X() / part.momentum().Z()

            if(part.mother() is None):
                continue

            
            
            #print 'Mother: ', part.particleID().pid()
            if( abs(part.particleID().pid()) == 211 ):
                pi_in_general+=1
                print 'Part= ',abs(part.particleID().pid()) ,  'Mother: ', abs(part.mother().particleID().pid())
                
        
            if( (abs(part.particleID().pid() == 211))  and (abs(part.mother().particleID().pid())== 413) ):
                nDstar+=1
                

                
            record = {
                'evt_index': i,
                    'x': hits[j].entry().x(),
                    'y': hits[j].entry().y(),
                    'z': hits[j].entry().z(),
                    't': hits[j].time(),
                    'x_disp': hits[j].displacement().x(),
                    'y_disp': hits[j].displacement().y(),
                    'z_disp': hits[j].displacement().z(),
                    'p': hits[j].p(),
                    'tx': tx,
                    'mc_particle': mcpid,
                    'pid': part.particleID().pid(),
                    'origin_x': part.originVertex().position().x(),
                    'origin_y': part.originVertex().position().y(),
                    'origin_z': part.originVertex().position().z(),
                    'det_id': hits[j].sensDetID(),
                }
            records.append(record)

        for i in range(len(mcparts)):
            part = mcparts[i]
            if not hasattr(part, 'particleID'):
                    continue
                
            
            #print '2nd loop', part.particleID().pid()
            if not hasattr(part, 'mother'):
                continue

            if(part.mother() is None):
                     continue

#            if(part.particleID().pid() != 13):
#                continue
#            ntau23mu+=1
            #print part.particleID().pid()
            if part.mother() and abs(part.mother().particleID().pid()) == 15:
                record = { 'pz': part.momentum().Pz(),
                           'p': part.momentum().P(),
                           'parent_p': part.mother().momentum().P(),
                           'has_ms_hit': i in hit_mcpids,
                           'has_ft_hit': i in hit_mcpids_ft,
                           'has_tt_hit': i in hit_mcpids_tt,
                           'has_vp_hit': i in hit_mcpids_vp }
                records_signal.append(record)

    except TypeError, e:
        print(e)
        break

    df = pd.DataFrame(records)
    df_signal = pd.DataFrame(records_signal)

    all_dfs.append(df)
    all_dfs_signal.append(df_signal)



print 'NDstar= ', float(nDstxar)/simulated
print 'pi in general= ', float(pi_in_general)/simulated



df = pd.concat(all_dfs)
df_signal = pd.concat(all_dfs_signal)
df.to_hdf('hits.h5', 'hits', mode='w')
df_signal.to_hdf('signal_data.h5', 'data', mode='w')

