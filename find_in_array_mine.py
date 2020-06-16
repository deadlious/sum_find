import sys
from datetime import datetime, timedelta
from random import randint, seed
from natsort import natsorted


def measure_time(original_function):
    def new_function(*args, **kwargs):
        a = datetime.now()
        ret = original_function(*args, **kwargs)  # the () after "original_function" causes original_function to be called
        b = datetime.now()
        c = b - a
        return ret, c
    return new_function


def binary_search(arr, low, high, x, esc=False):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x, esc)

            # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x, esc)

    else:
        # Element is not present in the array
        if esc:
            return low if high < 0 else high
        return -1


# @measure_time
def get_random_array():
    arr = list()
    seed(datetime.now())
    for b in range(randint(50000, 100000)):
        arr.append(randint(1, 1000000))
    return arr


@measure_time
def get_sorted_array(ar=None):
    if ar is None:
        ar = get_random_array()
    return natsorted(ar)


@measure_time
def find_num_evb(suma, ar=None, is_sorted=False, prnt=False):
    if not is_sorted or ar is None:
        ar = get_sorted_array(ar)
    b = binary_search(ar, 0, len(ar) - 1, suma, True)
    if b <= 0:
        if prnt:
            print('e: 404 Not Found')
        return False
    a = 0
    while True:
        s1 = ar[a] + ar[b]
        if s1 == suma:
            if prnt:
                print('e: Found a&b @', a, ',', b, ' = ', ar[a], ',', ar[b])
            return True
        elif s1 < suma:
            a += 1
        else:
            b -= 1
        if b == a or b < a:
            if prnt:
                print('e: 404 Not Found')
            return False


@measure_time
def find_num_bin(suma, ar=None, is_sorted=False, prnt=False):
    if not is_sorted or ar is None:
        ar = get_sorted_array(ar)
    l = len(ar) - 1
    for k, v in enumerate(ar):
        b = suma - v
        if b < v or k == l:
            return False
        if ar[l] == b:
            if prnt:
                print('b: Found a&b @', k, ',', l, ' = ', v, ',', ar[l])
            return True
        l = binary_search(ar, k + 1, l, b, True)
        if ar[l] == b:
            if prnt:
                print('b: Found a&b @', k, ',', l, ' = ', v, ',', ar[l])
            return True
    if prnt:
        print("b: 404 Not Found")
    return False


@measure_time
def compare_sums(times=1000):
    evb_time = timedelta()
    bin_time = timedelta()
    srt_time = timedelta()
    evb_wins, bin_wins = 0, 0
    found_a, found_b = 0, 0
    for i in range(times):
        ar, t = get_sorted_array()
        srt_time += t
        suma = randint(2, 1000000)
        # print('Sum to find: ', suma)
        suc_b, b = find_num_bin(suma, ar, True)
        suc_a, a = find_num_evb(suma, ar, True)
        evb_time = evb_time + a
        bin_time = bin_time + b
        if suc_a:
            found_a += 1
        if suc_b:
            found_b += 1
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
    print('EVB ', found_a, ':', found_b, ' BIN')



if __name__ == '__main__':

    print('Time elpased: ', compare_sums(int(sys.argv[1]) if len(sys.argv) > 1 else 1000)[1])
