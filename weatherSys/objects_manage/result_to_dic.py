

def to_dic(data, column):
    try:
        result = []
        for x in data:
            d = {}
            for index, y in enumerate(x):
                d[column[index]] = y
            result.append(d)
        return result
    except  Exception as e:
        print(e)
        return None