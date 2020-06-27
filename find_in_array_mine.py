import sys
from datetime import timedelta
from random import randint
from utils import measure_time, get_sorted_array, get_random_array, binary_search


@measure_time
def find_num_evb(suma, ar=None, is_sorted=False, prnt=False):
    # if not is_sorted or ar is None:
    #     ar = get_sorted_array(ar)
    b = binary_search(ar, 0, len(ar) - 1, suma - ar[0], True)
    if b <= 0:
        # if prnt:
        #     print('e: 404 Not Found')
        return False
    a = 0
    while True:
        s1 = ar[a] + ar[b]
        if s1 == suma:
            # if prnt:
            #     print('e: Found a&b @', a, ',', b, ' = ', ar[a], ',', ar[b])
            return True
        elif s1 < suma:
            a += 1
        else:
            b -= 1
        if b <= a:
            # if prnt:
            #     print('e: 404 Not Found')
            return False


@measure_time
def find_num_bin(suma, ar=None, is_sorted=False, prnt=False):
    # if not is_sorted or ar is None:
    #     ar = get_sorted_array(ar)
    l = len(ar) - 1
    k = 0
    for v in ar:
        b = suma - v
        if b < v or k == l:
            return False
        # if ar[l] == b:
            # if prnt:
            #     print('b: Found a&b @', k, ',', l, ' = ', v, ',', ar[l])
        #     return True
        l = binary_search(ar, k + 1, l, b, True)
        if ar[l] == b and k != l:
            # if prnt:
            #     print('b: Found a&b @', k, ',', l, ' = ', v, ',', ar[l])
            return True
        k += 1
    # if prnt:
    #     print("b: 404 Not Found")
    return False


@measure_time
def find_in_dict(suma, ar=None):
    br = dict()
    for b in ar:
        if (suma - b) in br:
            return True
        else:
            br[b] = True
    return False


@measure_time
def compare_sums(times=1000):
    evb_time = timedelta()
    bin_time = timedelta()
    srt_time = timedelta()
    dic_time = timedelta()
    evb_wins, bin_wins = 0, 0
    found_a, found_b, found_c = 0, 0, 0
    for i in range(times):
        dr = get_random_array()
        ar, t = get_sorted_array(dr)
        srt_time += t
        suma = randint(2, 40000)
        suc_b, b = find_num_bin(suma, ar, True)
        suc_a, a = find_num_evb(suma, ar, True)
        suc_c, c = find_in_dict(suma, dr)
        evb_time = evb_time + a
        bin_time = bin_time + b
        dic_time = dic_time + c
        if suc_a:
            found_a += 1
        if suc_b:
            found_b += 1
        if suc_c:
            found_c += 1
        if a < b and (suc_a or (not suc_b)):
            evb_wins += 1
        elif a > b and (suc_b or (not suc_a)):
            bin_wins += 1

        if suc_a ^ suc_b:
            print('Error with SUM: ', suma)
            find_num_bin(suma, ar, True, True)
            find_num_evb(suma, ar, True, True)

        # else it's a tie

    print('Sort AVG: ', srt_time / times)
    print('EVB faster: ', evb_wins, ", AVG: ", evb_time / times)
    print('BIN faster: ', bin_wins, ", AVG: ", bin_time / times)
    print('DIC AVG: ', dic_time / times, ', Found: ', found_c)
    print('Found: EVB ', found_a, ':', found_b, ' BIN')


if __name__ == '__main__':

    print('Time elapsed: ', compare_sums(int(sys.argv[1]) if len(sys.argv) > 1 else 1000)[1])
