import numpy as np

def getGender(agents_per_race, race):
    women_per_race = agents_per_race//2
    women_matrix = np.ones((women_per_race, race))
    men_matrix= np.zeros((women_per_race, race))
    leftovers = np.random.randint(low=0, high=2, size=(agents_per_race-2*women_per_race,race))# high is exclusive, generates 0 and 1
    gender_matrix = np.concatenate((women_matrix, men_matrix, leftovers))
    
    # generate random matrix to shuffle columns of gender_matrix
    rand_matrix = np.random.random(gender_matrix.shape)
    
    row_indices = np.argsort(rand_matrix, axis=0)
    
    # Preserve order of columns
    col_indices = np.arange(gender_matrix.shape[1])[None, :]
   
    gender_matrix = gender_matrix[row_indices, col_indices]
    
    return np.transpose(gender_matrix)

def createPersonality(agents_per_race, race, gender_matrix=None):
    if gender_matrix is None:
        social_beliefs = np.random.rand(race*agents_per_race)
        political_beliefs = np.random.rand(race*agents_per_race)
    else:
        mean_w = 0.25
        mean_m = 0.75
        social_beliefs_women = np.random.normal(loc=mean_w, scale=0.1, size=race*agents_per_race)
        political_beliefs_women = np.random.normal(loc=mean_w, scale=0.1, size=race*agents_per_race)
        social_beliefs_men = np.random.normal(loc=mean_m, scale=0.1, size=race*agents_per_race)
        political_beliefs_men = np.random.normal(loc=mean_m, scale=0.1, size=race*agents_per_race)

        gender_reshape = gender_matrix.reshape(race*agents_per_race)
        social_beliefs = np.where(gender_reshape==1, social_beliefs_women, social_beliefs_men)
        political_beliefs = np.where(gender_reshape==1, political_beliefs_women, political_beliefs_men)
        
    return (social_beliefs, political_beliefs)

def createAdj(agents_per_race, race, prob_inter=0.4, prob_intra=0.7):
    agents = agents_per_race*race
    adj= np.zeros((agents,agents))
    
    #Interracial edges
    max_inter = int(((race-1)*race/2)*agents_per_race**2)
    num_inter = int(max_inter*prob_inter)
    inter_edges = np.random.choice(max_inter, size=(1,num_inter), replace=False)
    inter_edge = 0
    for i in range(agents):
        prev_race = i//agents_per_race
        for j in range(prev_race*agents_per_race+agents_per_race, agents):
            if (i != j):
                if np.any(inter_edges == inter_edge):
                    adj[i,j] = 1
                inter_edge +=1    
                
    #Intraracial edges
    intra_edges = np.random.rand(agents,agents)
    for i in range(agents):
        current_race = i//agents_per_race
        for j in range (i+1, current_race*agents_per_race+agents_per_race):           
            if (intra_edges[i,j] < prob_intra):
                adj[i,j] = 1
                
    #Reflect triangle
    adj = np.triu(adj,0)+np.transpose(np.triu(adj))
    
    #Get all connections of at least distance 2 (at least one mutual friend)
    adj2 = np.matmul(adj,adj)
    
    #Directly connected or have at least one mutual friend
    adj3 = (adj+adj2>0).astype(int)
    np.fill_diagonal(adj3, 0)
    
    return adj,adj2,adj3

def getPersonalityDistances(agents, adjacency, genders, social_beliefs, political_beliefs, bisexuals=False):
    distance = np.zeros((agents,agents))
    gender_vector = genders.reshape((agents))
    
    for i in range(agents):
        for j in range(i, agents):
            # Same person
            if (i==j):
                distance[i, j] = np.inf
            elif (adjacency[i,j]==0):
                distance[i,j] = np.inf
            elif (not bisexuals and gender_vector[i] == gender_vector[j]):
                distance[i, j] = np.inf
            else: 
                political_diff = political_beliefs[i] - political_beliefs[j]
                social_diff = social_beliefs[i] - social_beliefs[j]
                distance[i,j] = np.sqrt(political_diff**2 + social_diff**2)
    distance = np.triu(distance, 0)+np.transpose(np.triu(distance))
    return distance

def createMarriages(agents, distances, genders):
    dist_copy = np.copy(distances)
    marriage = np.zeros(agents)
    marriage.fill(-1)
    
    women = np.sum(genders)
    men= agents-np.sum(genders)
    max_either_sex = int(max(women, men))
    best_match = np.argmin(dist_copy, axis=1)
    counter = 0
    
    for n in range(max_either_sex):
        for i in range(agents):
            crush = best_match[i]
            not_strangers = dist_copy[i, crush] != np.inf and dist_copy[crush,i] != np.inf
            if (i == best_match[crush] and not_strangers):
                marriage[i] = crush
        for j in range(agents):
            if (marriage[j]<0):
                if (marriage[best_match[j]] >= 0):
                    dist_copy[j, best_match[j]] = np.inf

        best_match = np.argmin(dist_copy, axis=1)
    
    return (marriage.astype(int),distances)

def averageDistances(distances, marriage):
    avg_dist = 0;
    for i in marriage:
        if (i >= 0):
            avg_dist += distances[i, marriage[i]]

    # Number of married people
    num_marriage = np.sum([marriage>=0])
    return(avg_dist/num_marriage)

def numIntraracial(marriage, agents_per_race, races):
    agents = agents_per_race*races
    num_intra = 0
    for i in range(agents):
        if (marriage[i] >=0):
            curr_race = i//agents_per_race
            race_end = (1+curr_race) * agents_per_race
            race_start = curr_race*agents_per_race
            if ((marriage[i] < race_end) and (marriage[i]>=race_start)):
                num_intra += 1
    return num_intra/2

def numInterracial(num_intra, marriage):
    # Number of marriages
    num_marriage = np.sum([marriage>=0])/2
    return(num_marriage - num_intra) 

def welfareRatios(num_intra, num_inter, marriage, races, agents_per_race, avg_dist):
    num_marriage = np.sum([marriage>=0])/2
    
    #ratio of people in interracial marriages to some race thing
    
    #TODO what is this
    r1 = (num_inter/num_marriage)/((races-1)/races)
        
    #ratio of people in marriages to total people
    r2 = num_marriage*2/(agents_per_race*races)
    
    #Normalized compatibility
    r3 = (np.sqrt(2)-avg_dist)/np.sqrt(2)
    
    return(r1,r2,r3)

def genderRatios(marriage, agents, gender_matrix):
    mw = 0
    mm = 0
    ww = 0

    gender_reshape = gender_matrix.reshape(agents)
    for agent in range(agents):
        gender1 = gender_reshape[agent]
        gender2 = gender_reshape[marriage[agent]]

        if gender1 == 0 and gender1 == gender2:
            mm+=1
        elif gender1 == 1 and gender1 == gender2:
            ww+=1
        else:
            mw+=1
    return mw, mm, ww

def runSim(agents_per_race, races, prob_intra, prob_inter, marr_type=1):
    agents = agents_per_race*races
    genders=getGender(agents_per_race,races)
    social_beliefs, political_beliefs = createPersonality(agents_per_race, races)
    adj, adj2, adj3 = createAdj(agents_per_race, races, prob_inter=prob_inter, prob_intra=prob_intra)
    network = adj if marr_type == 1 else adj3
    distances = getPersonalityDistances(agents, network, genders, social_beliefs, political_beliefs)
    marriage, distances = createMarriages(agents, distances,genders)
    avg_dist = averageDistances(distances, marriage)
    num_intra = numIntraracial(marriage, agents_per_race, races)
    num_inter = numInterracial(num_intra, marriage)
    diversity,percent_married,compatibility = welfareRatios(num_intra, num_inter, marriage, races, agents_per_race, avg_dist)
    return diversity,percent_married,compatibility