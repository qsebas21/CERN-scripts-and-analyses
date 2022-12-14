#lb-run -l -c best Gauss
#lb-run -c best Gauss/v55r2 ipython

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
EventSelector().Input = ["DATA='PFN:/afs/cern.ch/work/j/jmalczew/public/Lcstar2Lcpipi_1000ev_noPacking.sim' SVC='Gaudi::RootEvtSelector'"]
EventSelector().PrintFreq = 1
MessageSvc().OutputLevel = 3

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()
appMgr.run(1)

def nodes(evt, root='/Event'):
    """List all nodes in `evt` starting from `node`."""
    node_list = [root]
    for leaf in evt.leaves(evt[root]):
        node_list += nodes(evt, leaf.identifier())
    return node_list

nodes(evt)


#hit = hits[0]
#hit.mcParticle()
#hit.mcParticle().mother().particleID().pid()
#p = hit.mcParticle().mother()
#

#parts[p.index()] == p

vp_hits = evt['/Event/MC/VP/Hits']
parts = evt['/Event/MC/Particles']

#count velo events

velo_indices = list()  
for i in range(len(vp_hits)):  
   	if vp_hits[i].mcParticle().particleID().pid() != 11:  
       	continue
   	for j in range(len(vp_hits)):
       	if vp_hits[j].mcParticle().particleID().pid() == -11 and vp_hits[i].mcParticle().mother().index() == vp_hits[j].mcParticle().mother().index() and vp_hits[i].mcParticle().mother().particleID().pid() == 22 and vp_hits[i].mcParticle().mother().index() not in velo_indices:  
           	velo_indices.append(vp_hits[i].mcParticle().mother().index())
print('Events in VELO: ' + str(len(velo_indices))) 

#count total events
total_gamma_to_ee = 0 
#
#decay_indices = list()
for i in range(len(parts)): 
    if parts[i].particleID().pid() != 11: 
        continue 
    for j in range(len(parts)): 
        if parts[j].particleID().pid() == -11 and parts[i].mother().index() == parts[j].mother().index() and parts[i].mother().particleID().pid() == 22: 
            total_gamma_to_ee += 1
            decay_indices.append(i)
print('Total decays: ' + str(total_gamma_to_ee))

print('Fraction VELO/total: ' + str(velo_gamma_to_ee/total_gamma_to_ee))


#y_pos = np.empty_like(parts)
#z_pos = np.empty_like(parts)
#  
#for i in decay_indices: 
#    y_pos[i] = parts[i].originVertex().position().y() 
#    z_pos[i] = parts[i].originVertex().position().z() 
#      
#plt.scatter(y_pos, z_pos, 0.5, alpha=0.25)



## find Lc and figure out mothers 
Lc_indices = list()


lc_count = 0

for j in range(1000):
	appMgr.run(1)
	parts = evt['/Event/MC/Particles']
	for i in range(len(parts)):
        if abs(parts[i].particleID().pid()) == 4122:
            lc_count += 1
			print('Particle index: ' + str(parts[i].index()))
    	    print('Mother:')        
    	    print(parts[i].mother())


print(lc_count)


#create dict with key value pair {'particle index': 'list of particle IDs of daughters'}

daughtersList = dict()

for i in parts:
    daughters = list()
    for j in parts:
        try:
            if j.mother().index() == i.index():
                daughters.append(j.particleID().pid())
        except:
            continue
    daughtersList[i.index()] = daughters
    
daughtersList
    
indices = list()
for i in parts:
    if abs(i.particleID().pid()) != 4122:
        continue
        
    try:
        if abs(i.mother().particleID().pid()) == 4214 and 211 in daughtersList[i.mother().index()] and 211 in daughtersList[i.mother().index()] and (2122 in daughtersList[i.index()] or -2122 in daughtersListdaughtersList[i.index()]) and (321 in daughtersList[i.index()] or -321 in daughtersListdaughtersList[i.index()]) and (211 in daughtersList[i.index()] or -211 in daughtersListdaughtersList[i.index()]) and i.index() not in indices:
            indices.append(i.index())
    except:
        continue
        
        
