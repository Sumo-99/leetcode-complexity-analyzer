class Solution:
    def minimizeMax(self, nums, p):
        if p == 0:
            return 0
        nums.sort()
        n = len(nums)
        left, right = 0, nums[-1] - nums[0]
        while left < right:
            mid = left + (right - left) // 2
            pairs = 0
            i = 1
            while i < n:
                if mid >= nums[i] - nums[i - 1]:
                    pairs += 1
                    i += 1
                i += 1
            if pairs >= p:
                right = mid
            else:
                left = mid + 1
        return left
