from textblob import TextBlob
def scoring(score, comment, distributorName, certified,stlName,seedGrowerName, lotID, orderID):
    """
    score: score provided by farmer
    """
    if score <= 2:
        if certified == 'No':
            stlScore = 2
            distributorScore = 0
            seedGrower = score
        if certified == 'Yes':
            stlScore = 0
            distributorScore = 1
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
    testimonial = TextBlob(comment)
    sent = testimonial.sentiment
    return {stlName:stlScore, distributorName:distributorScore, seedGrowerName:seedGrower,"sentiment":sent}