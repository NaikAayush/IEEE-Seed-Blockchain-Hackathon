def soil_fertility(fi, fs):
    """Obtain Firtility Class from fertility Index"""
    try:
        if fi < 1.67:
            fertility_status = "low"
        if fi<=2.33 and fi>=1.67:
            fertility_status =  "medium"
        
        else:
            fertility_status = "high"
            
        if fertility_status == fs.lower():
            trust = 1
        else:
            if fertility_status == "low" and fs.lower=="high":
                trust = 0
            else:
                trust = 0.5
        return calculatedFertilityStatus, calculatedTrust
     
    except Exception as e:
        return str(e),''
