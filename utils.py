from natsort import natsorted
from datetime import datetime
from random import randint, seed


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


@measure_time
def mergesort(dataset):
    if len(dataset) > 1:
        mid = len(dataset) // 2
        leftarr = dataset[:mid]
        rightarr = dataset[mid:]

        # split
        mergesort(leftarr)
        mergesort(rightarr)

        i = 0  # left
        j = 0  # right
        k = 0  # new

        while i < len(leftarr) and j < len(rightarr):
            if leftarr[i] < rightarr[j]:
                dataset[k] = leftarr[i]
                i += 1
            else:
                dataset[k] = rightarr[j]
                j += 1
            k += 1

        while i < len(leftarr):
            dataset[k] = leftarr[i]
            i += 1
            k += 1

        while j < len(rightarr):
            dataset[k] = rightarr[j]
            j += 1
            k += 1


@measure_time
def quicksort(dataset, first, last):
    if first < last:
        pivotIdx = partition(dataset, first, last)

        quicksort(dataset, first, pivotIdx - 1)
        quicksort(dataset, pivotIdx + 1, last)


def partition(dataval, first, last):
    pivotval = dataval[first]

    lower = first + 1
    upper = last

    done = False
    while not done:
        while lower <= upper and dataval[lower] <= pivotval:
            lower += 1
        while dataval[upper] >= pivotval and upper >= lower:
            upper -= 1

        if upper < lower:
            done = True
        else:
            temp = dataval[lower]
            dataval[lower] = dataval[upper]
            dataval[upper] = temp

    temp = dataval[first]
    dataval[first] = dataval[upper]
    dataval[upper] = temp

    return upper


# @measure_time
def get_random_array(nmin=500, nmax=1000, lim=10000):
    arr = list()
    seed(datetime.now())
    for b in range(randint(nmin, nmax)):
        arr.append(randint(1, lim))
    return arr


@measure_time
def get_sorted_array(ar=None):
    if ar is None:
        ar = get_random_array()
    return natsorted(ar)

