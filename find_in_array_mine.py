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


def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

            # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


# @measure_time
def get_random_array():
    arr = list()
    seed(datetime.now())
    for b in range(randint(5000, 10000)):
        arr.append(randint(1, 20000))
    return arr


# @measure_time
def get_sorted_array(ar=None):
    if ar is None:
        ar = get_random_array()
    return natsorted(ar)


@measure_time
def find_num_evb(suma, ar=None, is_sorted=False):
    br = list()
    if not is_sorted or ar is None:
        ar = get_sorted_array(ar)
    for i in ar:
        if i < suma:
            br.append(i)
        else:
            break
    b = len(br) - 1
    if b < 0:
        return False
    a = 0
    while True:
        s1 = br[a] + br[b]
        if s1 == suma:
            # print('Found a&b @', a, ',', b, ' = ', br[a], ',', br[b])
            return True
        elif s1 < suma:
            a += 1
        else:
            b -= 1
        if b == a or b < a or b < 1 or a == len(br):
            # print('404 Not Found')
            return False


@measure_time
def find_num_bin(suma, ar=None, is_sorted=False):
    if not is_sorted or ar is None:
        ar = get_sorted_array(ar)
    l = len(ar) - 1
    for k, v in enumerate(ar):
        b = suma - v
        if b < 1:
            # print("404 Not Found")
            return False
        if ar[l] == b:
            # print('Found a&b @', "-0", ',', l, ' = ', v, ',', ar[l])
            return True
        if (binary_search(ar, k, l, b)) > -1:
            # print('Found a&b @', k, ',', f, ' = ', v, ',', ar[f])
            return True
    # print("404 Not Found")
    return False


def compare_sums(times=1000):
    evb_time = timedelta()
    bin_time = timedelta()
    evb_wins, bin_wins = 0, 0
    for i in range(times):
        ar = get_sorted_array()
        suma = randint(2, 39999)
        suc_a, a = find_num_evb(suma, ar, True)
        suc_b, b = find_num_bin(suma, ar, True)
        evb_time = evb_time + a
        bin_time = bin_time + b

        if (a < b and suc_a) or ((not suc_b) and a < b):
            evb_wins += 1
        elif (a > b and suc_b) or ((not suc_a) and a > b):
            bin_wins += 1
        # else it's a tie

    print('EVB: ', evb_wins, ", AVG: ", evb_time / times)
    print('BIN: ', bin_wins, ", AVG: ", bin_time / times)


if __name__ == '__main__':

    compare_sums(int(sys.argv[1]) if len(sys.argv) > 1 else 1000)
