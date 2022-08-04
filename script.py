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
EventSelector().Input = ["DATA='PFN:/afs/cern.ch/work/j/jmalczew/public/Lcstar2Lcpipi_100ev_noPacking.sim' SVC='Gaudi::RootEvtSelector'"]
EventSelector().PrintFreq = 1
MessageSvc().OutputLevel = 3

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()

import numpy as np


#find amount of Lc particles in the file



for j in range(simulated):
	appMgr.run(1)
	parts = evt['/Event/MC/Particles']
	
	for i in range(len(parts)):
        if abs(parts[i].particleID().pid()) == 4122:
            lc_count += 1

print(lc_count)

#alright let's get this bread

total_gain = 0

simulated = 1000

for k in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    vp_hits = evt['/Event/MC/VP/Hits']
    ms_hits = evt['/Event/MC/MS/Hits']
    #ot_hits = evt['/Event/MC/OT/Hits']
    vpparts = []
    for i in vp_hits:
        vpparts[i] = vp_hits[i].mcParticle()
    msparts = []
    for i in ms_hits:
        msparts[i] = ms_hits[i].mcParticle()    
#    otparts = []
#    for i in ot_hits:
#        otparts[i] = ot_hits[i].mcParticle()    
        
    d_vp = 0
    d_ms = 0
    #d_ot = 0
    
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
    
    #find velo decays for this event
    
    vp_indices = list() #list of unique decays
    
    for i in vp_hits:
        #find Lc parts
        
        if abs(i.mcParticle().particleID().pid()) != 4122:
            continue
        
        #now, check for these requirements: 
        #mother is a Lcstar
        #mother has pi+ and pi- daughters
        #Lc has proton or antiproton daughter
        #Lc has K- or K+ daughter
        #Lc has pi- or pi+ daughter 
        #this decay hasn't already been counted.
        
        try:
            if abs(i.mcParticle().mother().particleID().pid()) == 4214 and 211 in daughtersList[i.mcParticle().mother().index()] and 211 in daughtersList[i.mcParticle().mother().index()] and (2122 in daughtersList[i.mcParticle().index()] or -2122 in daughtersList[i.mcParticle().index()]) and (321 in daughtersList[i.mcParticle().index()] or -321 in daughtersListdaughtersList[i.mcParticle().index()]) and (211 in daughtersList[i.mcParticle().index()] or -211 in daughtersList[i.mcParticle().index()]) and i.mcParticle().index() not in vp_indices:
                vp_indices.append(i.mcParticle().index())
        except:
            continue
    d_vp = len(vp_indices)
    
    #find ms decays for this event, same idea as vp
    
    ms_indices = list()
    for i in ms_hits:
        #find Lc parts
        
        if abs(i.mcParticle().particleID().pid()) != 4122:
            continue
        
        #now, check for these requirements: 
        #mother is a Lcstar
        #mother has pi+ and pi- daughters
        #Lc has proton or antiproton daughter
        #Lc has K- or K+ daughter
        #Lc has pi- or pi+ daughter 
        #this decay hasn't already been counted.
        
        try:
            if abs(i.mcParticle().mother().particleID().pid()) == 4214 and 211 in daughtersList[i.mcParticle().mother().index()] and 211 in daughtersList[i.mcParticle().mother().index()] and (2122 in daughtersList[i.mcParticle().index()] or -2122 in daughtersList[i.mcParticle().index()]) and (321 in daughtersList[i.mcParticle().index()] or -321 in daughtersListdaughtersList[i.mcParticle().index()]) and (211 in daughtersList[i.mcParticle().index()] or -211 in daughtersList[i.mcParticle().index()]) and i.mcParticle().index() not in ms_indices:
                ms_indices.append(i.mcParticle().index())
        except:
            continue
            
    d_ms = len(ms_indices)
    
#    #find ot decays for this event
#    
#    for i in ot_hits:
#        #find Lc parts
#        
#        if abs(i.mcParticle().particleID().pid()) != 4122:
#            continue
#        
#        #now, check for these requirements: 
#        #mother is a Lcstar
#        #mother has pi+ and pi- daughters
#        #Lc has proton or antiproton daughter
#        #Lc has K- or K+ daughter
#        #Lc has pi- or pi+ daughter 
#        #this decay hasn't already been counted.
#        
#        try:
#            if abs(i.mcParticle().mother().particleID().pid()) == 4214 and 211 in daughtersList[i.mcParticle().mother().index()] and 211 in daughtersList[i.mcParticle().mother().index()] and (2122 in daughtersList[i.mcParticle().index()] or -2122 in daughtersList[i.mcParticle().index()]) and (321 in daughtersList[i.mcParticle().index()] or -321 in daughtersListdaughtersList[i.mcParticle().index()]) and (211 in daughtersList[i.mcParticle().index()] or -211 in daughtersList[i.mcParticle().index()]) and i.mcParticle().index() not in ot_indices:
#                ot_indices.append(i.mcParticle().index())
#        except:
#            continue
#
#    d_ot = len(ot_indices)
    
    #calculate gain for this event

    try:
        gain = (d_vp + d_ms)/d_vp # + d_ot
        print('VP decays: ' + str(d_vp) + '. MS decays: ' + str(d_ms) '. Event ' + str(k) + ' gain: ' + str(gain))
        total_gain = total_gain + gain
    except: 
        print('Event ' + str(k) + ': error (probably no numerator decays)')
    

average = total_gain/simulated

print('The average gain is ' + str(average))
