import heapq
import numpy as np
def findKthLargest(nums, k):
    h = []
    for n in nums:
        if len(h) < k:
            heapq.heappush(h, n)
        else:
            heapq.heappushpop(h, n)
    return h[0]