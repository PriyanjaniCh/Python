# Python3
# August LeetCode Challenge - Day 3
# Valid Palindrome

# Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.
# Note: For the purpose of this problem, we define empty string as valid palindrome.

# Constraints:
# s consists only of printable ASCII characters.

class Solution:
    def isPalindrome(self, s: str) -> bool:
        s1 = ''.join(st for st in s if st.isalnum())
        if s1.lower() == s1[::-1].lower():
            return True
        else:
            return False
        
        
