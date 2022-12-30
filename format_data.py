def save_data(data):
    return {
        "data": data,
    }

def send_data(jam, menit, data):
    return {
        'time' : "{}:{}".format(str(jam), str(menit)),
        'data' : data
    }