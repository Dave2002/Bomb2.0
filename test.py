
stripRGB = (0.0 ,255.0 ,255)
stripeBlinkerStop = False

#while not stripeBlinkerStop:
tmp = [0,0,0]
tmp[0] = stripRGB[0]
tmp[1] = stripRGB[1]
tmp[2] = stripRGB[2]
while sum(tmp) > 69:
    tmp[0] = min(tmp[0] - tmp[0] * 0.1,255)
    tmp[1] = min(tmp[1] - tmp[1] * 0.1,255)
    tmp[2] = min(tmp[2] - tmp[2] * 0.1,255)
    print(tmp)
while sum(tmp) <250:
    print("wechsel")
    tmp[0] = min(tmp[0] + tmp[0] * 0.1,255)
    tmp[1] = min(tmp[1] + tmp[1] * 0.1,255)
    tmp[2] = min(tmp[2] + tmp[2] * 0.1,255)
    print(tmp)
