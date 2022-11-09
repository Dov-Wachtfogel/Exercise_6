def get_analyze(get_message_path: str):
    l = get_message_path.split('?')
    path = l[0]
    parms = l[1]
    parms_dict = eval('{"' + parms.replace('&', '","').replace('=', '":"') + '"}')
    for key in parms_dict:
        if parms_dict[key].isnumeric():
            parms_dict[key] = float(parms_dict[key])
    return path, parms_dict

#print(get_analyze('/hello?a=5&b=3'))
dict = {1:2, 3:4}
print(list(dict.values()))