import array_set as aset

array_mid = aset.array_mid_1
mid_1 = aset.mid_len_1
mid = aset.mid_len_2

def detect(degree):
    if -180.000000 <= degree < -178.808000 and 178.808000 < degree < 180.000000:
        array_mid.append(1)
    return array_mid