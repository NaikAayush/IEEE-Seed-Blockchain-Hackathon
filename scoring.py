def scoring(score, distributorID, certified):
    if score <= 2:
        if certified == 'No':
            stlScore = 2
            distributorScore = -5
            seedGrower = score
        if certified == 'Yes':
            stlScore = -5
            distributorScore = 2
            seedGrower = score
    else if score >= 4:
        if certified == 'Yes':
            stlScore = 5
            distributorScore = 5
            seedGrower = score
        else certified == 'No':
            stlScore = 2
            distributorScore = 2
            seedGrower = score
    else:
        stlScore = 3
        distributorScore = 3
        seedGrower = 3
    return stlScore, distributorScore
        
        
        
               