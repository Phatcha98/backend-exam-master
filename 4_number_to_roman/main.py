"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""
number = int(input("input a number: "))

class Solution:

    def number_to_roman(self, number: int) -> str:
        if number <= 0:
            return "number can not less than 0"
        
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL","X", "IX", "V", "IV", "I"]

        roman_text = ""
        for i, v in enumerate(val):
            while number >= v:
                roman_text += syms[i]
                number -= v
        return roman_text
    
solution = Solution()
print(solution.number_to_roman(number))