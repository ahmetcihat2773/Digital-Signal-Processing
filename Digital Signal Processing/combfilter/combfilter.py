def combfilter(b,a,factor):
    """
    Add coefficients and zeros into a new list for each a and b. 
    """
    temp_a = list()
    temp_b = list()
    try:            
        if len(a)>1:
            # If a is an array which is the case for IIR filters.
            for m in range(len(b)):
                temp_b.append(b[m])
                temp_a.append(a[m])
                for i in range(factor):
                    temp_b.append(0)
                    temp_a.append(0)
            return temp_b,temp_a 
    except:
        for m in range(len(b)):
            # if a is an integer which is the case for FIR filter in this program.
            temp_b.append(b[m])
            for i in range(factor):
                temp_b.append(0)
        return temp_b,a
    
