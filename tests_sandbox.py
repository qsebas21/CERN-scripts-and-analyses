#check if there's lambda_c* and antilambda_c* in the same event (works?)
evts_with_both = 0
evts = list()
for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']


    has_Lc = False
    has_antiLc= False
    for j in parts:
        if j.particleID().pid() == 4214:
            has_Lc = True
            
        if j.particleID().pid() == -4214:
            has_antiLc = True
            
            
    if has_antiLc is True and has_Lc is True:
        evts_with_both += 1
        evts.append(event+1)
        print('Event ' + str(event + 1) + ' has anti-Lcstar and Lcstar.')


print('There are ' + str(evts_with_both) + ' events with both. The events are:')
print(evts)
     
#check what particles are there (with pid between 4000 and 4500) and how many (works)
totalParts = dict()

for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']

    partList = dict()
    for i in parts:
        if i.particleID().pid() < 4500 and i.particleID().pid() > 4000:
            if i.particleID().pid() in partList:
                partList[i.particleID().pid()] += 1
            else:
                partList[i.particleID().pid()] = 1
            if i.particleID().pid() in totalParts:
                totalParts[i.particleID().pid()] += 1 
            else:
                totalParts[i.particleID().pid()] = 1
    print('\nEvent: ' + str(event))
    print(partList)
    
print('The total is:')
print(totalParts)


#check if there's two Lc_star
mults = 0
mult = list()
for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    
    Lcstars = 0
    antis = 0
    
    for i in parts:
        pid = i.particleID().pid()
        if pid == 4214:
            Lcstars += 1
        if pid == -4214:
            antis += 1
    
    if Lcstars > 2 or antis > 2:
        mults += 1
        mult.append(event + 1)
    
print(str(mults) + ' multiples')
print('Events:')
print(mult)

    

#plot origin vertices of particles (works)
%matplotlib
import matplotlib.pyplot as plt

z_pos = list()
y_pos = list()

for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    
    for i in parts:
        if i.originVertex().position().z() < 20000 and i.originVertex().position().z() > -2000 and i.originVertex().position().y() > -6000 and i.originVertex().position().y() < 6000:
            z_pos.append(i.originVertex().position().z())
            y_pos.append(i.originVertex().position().y())

plt.scatter(z_pos, y_pos, s=0.1, alpha=0.1)

#create a dictionary with the daughters of Lc_star only (doesn't work, .sim file broken)
daughtersLc = dict()

for i in parts:
    i_index = i.index()
    pid = i.particleID().pid()
    if abs(pid) == 4214 or abs(pid) == 4122:
        daughters = set()
        for j in parts:
            try:
                if j.mother().index() == i_index:
                    daughters.append(j.particleID().pid())
            except:
                continue
        daughtersLc[i.index()] = daughters
            
            
# reconstruct decays (doesn't work)
for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    vp_hits = evt['/Event/MC/VP/Hits']
    ms_hits = evt['/Event/MC/MS/Hits']
    
    vp_decs = 0
    ms_decs = 0
    
    #make daughters dictionary
    daughtersLc = dict()

    for i in vp_hits:
        pid = i.mcParticle().particleID().pid()
        if i.mcParticle().index() not in daughtersLc.keys() and (abs(pid) == 4214 or abs(pid) == 4122):
            daughters = set()
            for j in vp_hits:
                try:
                    if j.mother().index() == i.index():
                        daughters.add(j.mcParticle().particleID().pid())
                except:
                    continue
            daughtersLc[i.mcParticle().index()] = daughters


    #now try to reconstruct everything lol
    

# write file(s) with background data and vp/ms/ut_hits (works)
%matplotlib 
import matplotlib.pyplot as plt

f1 = open('vertices.txt', 'w')
f2 = open('vp_hits.txt', 'w')
f3 = open('ms_hits.txt', 'w')
f4 = open('ut_hits.txt', 'w')

for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    vp_hits = evt['/Event/MC/VP/Hits']
    ms_hits = evt['/Event/MC/MS/Hits']
    ut_hits = evt['/Event/MC/UT/Hits']
    
    uniqueVerts = list()
    
    for i in parts:
        vert = i.originVertex()
        if vert not in uniqueVerts:
            uniqueVerts.append(vert)
            x, y, z = vert.position().x(), vert.position().y(), vert.position().z() 
            f1.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')
    
    for i in vp_hits:
        x, y, z = i.entry().Coordinates().x(), i.entry().Coordinates().y(), i.entry().Coordinates().z()
        f2.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')

    for i in ms_hits:
        x, y, z = i.entry().Coordinates().x(), i.entry().Coordinates().y(), i.entry().Coordinates().z()
        f3.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')

    for i in ut_hits:
        x, y, z = i.entry().Coordinates().x(), i.entry().Coordinates().y(), i.entry().Coordinates().z()
        f4.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')        
    
f1.close()
f2.close()
f3.close()
f4.close()

#find if there are usable (Lc to p K pi) decays

vp_decs = 0
ut_decs = 0
ms_decs = 0


for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    vp_hits = evt['/Event/MC/VP/Hits']
    ms_hits = evt['/Event/MC/MS/Hits']
    ut_hits = evt['/Event/MC/UT/Hits']
    
    unique_Lc = list()    
    for i in parts:
        pid = i.particleID().pid()
        i_index = i.index()
        if i_index not in unique_Lc and abs(pid) == 4122:
            unique_Lc.append(i_index)
            daughters = set()
            
            for j in vp_hits:
                try:
                    if j.mcParticle().mother().index() == i_index:
                        daughters.add(abs(j.mcParticle().particleID().pid())) #append won't work
                except:
                    continue
                
                if len(daughters) == 3:
                    break
                    
            if 2212 in daughters and 211 in daughters and 321 in daughters:
                vp_decs += 1
                #print('Mother is particle ' + str(i_index) + '. Daughters are')
                #print(daughters)
                
            daughters = set()
            
            for k in ut_hits:
                try:
                    if j.mcParticle().mother().index() == i_index:
                        daughters.add(abs(j.mcParticle().particleID().pid())) #append won't work
                except:
                    continue
                
                if len(daughters) == 3:
                    break
                    
            if 2212 in daughters and 211 in daughters and 321 in daughters:
                ut_decs += 1
                #print('Mother is particle ' + str(i_index) + '. Daughters are')
                #print(daughters)
                
            daughters = set()
            
            for l in ms_hits:
                try:
                    if j.mcParticle().mother().index() == i_index:
                        daughters.add(abs(j.mcParticle().particleID().pid())) #append won't work
                except:
                    continue
                
                if len(daughters) == 3:
                    break
                    
            if 2212 in daughters or 211 in daughters or 321 in daughters:
                ms_decs += 1
                #print('Mother is particle ' + str(i_index) + '. Daughters are')
                #print(daughters)
                
print('There are ' + str(vp_decs) + ' decays in VP.')
print('There are ' + str(ut_decs) + ' decays in UT.')
print('There are ' + str(ms_decs) + ' decays in MS.')

if vp_decs + ut_decs == 0:
    print('No decays in VP + UT.')
else:
    print('The total gain is ' + str(1 + ms_decs/(vp_decs + ut_decs)))
    
    
    
#check for full (Lc* to (Lc to pKpi) pi pi) decays (surface level) 
good_decs = 0
for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    
    
    #makes dictionary of daughters only of LcStar and Lc (and antiparticles)
    daughtersLc = dict()
    for i in parts:
        i_index = i.index()
        pid = i.particleID().pid()
        if abs(pid) == 4214 or abs(pid) == 4122:
            daughters = set()
            for j in parts:
                try:
                    if j.mother().index() == i_index:
                        daughters.add(j.particleID().pid())
                except:
                    continue
                if len(daughters) == 3:
                    break
            daughtersLc[pid] = daughters
    
    #if daughtersLc is not False:
    #    print('\nEvent:' + str(event + 1))        
    #    print(daughtersLc)
    
    sign = 1
    if -4214 in daughtersLc.keys():
        sign = -1
        
    if 4214 not in daughtersLc.keys() and -4214 not in daughtersLc.keys():
        print('Event ' + str(event + 1) + 'has no Lcstar or antiLcstar')
        continue
    
    if sign*4122 in daughtersLc[sign*4214]\
        and -sign*211 in daughtersLc[sign*4214]\ 
        and sign*2212 in daughtersLc[sign*4122]\
        and ((211 in daughtersLc[sign*4122] and -321 in daughtersLc[sign*4122])\
             or (-211 in daughtersLc[sign*4122] and 321 in daughtersLc[sign*4122])):
        good_decs += 1

    
print('There are ' + str(good_decs) + ' good decays.')


### finally

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
        if abs(pid) in good_pids:
            vp_parts.add(i.mcParticle())

    ut_parts = set()
    for i in ut_hits:
        i_pid = i.mcParticle().particleID().pid()
        if abs(pid) in good_pids:
            ut_parts.add(i.mcParticle())
                    
    ms_parts = set()
    for i in ms_hits:
        i_pid = i.mcParticle().particleID().pid()
        if abs(pid) in good_pids:
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
                
print('There are ' + str(vp_decs) + ' decays in VP.')
print('There are ' + str(ut_decs) + ' decays in UT.')
print('There are ' + str(ms_decs) + ' decays in MS.')

if vp_decs + ut_decs == 0:
    print('No decays in VP + UT.')
else:
    print('The total gain is ' + str(1 + ms_decs/(vp_decs + ut_decs)))
    
%history -o -f output.txt
