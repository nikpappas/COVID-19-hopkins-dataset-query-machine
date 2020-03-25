def differentiate_distinct(dictionary, prevKeyFunc):
    res = {}
    for key in dictionary:
        prevKey = prevKeyFunc(key)
        if prevKey not in dictionary:
            res[key] = dictionary[key]
        else:
            res[key] = dictionary[key] - dictionary[prevKey]
    return res

