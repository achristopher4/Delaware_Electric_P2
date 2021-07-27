## ## This document will be used to search with different search techniques
## Author: Alexander Christopher
## Date: 07/27/2021

class BinarySearch:
    def __init__(self, obj, target):
        """ Initialize BinarySearch. obj MUST BE SORTED IF NOT ALREADY. """
        length = len(obj)
        mid = len(obj) // 2
        start = 0
        end = length
        found = [False]
        while start != mid:
            #print(obj[mid], start, mid, end)
            if obj[mid] == target:
                found = [True, obj[mid]]
                break
            if obj[mid] < target:
                start = mid
                mid = (start + end) // 2
            elif obj[mid] > target:
                end = mid
                mid = (start + end) // 2
        return found
