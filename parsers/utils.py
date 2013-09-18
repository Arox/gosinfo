#from utf special symbol to utf text
dict_normal = {
    '\r':'',
    '\n':'',
    '\xd8':' диаметр ',
    '\u2015':' - '
}
def normalUtf(oldstr):
    newstr = oldstr
    for key in dict_normal.keys():
        newstr = newstr.replace(key, dict_normal[key])
    return newstr
