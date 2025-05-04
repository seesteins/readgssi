import readgssi.dzt
path = "/home/tetonicus/Projects/toolkit/inputs/FILE40.DZT"
meta, data, gps = readgssi.dzt.readdzt(path, verbose = True)
print(meta)
print(data)