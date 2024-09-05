"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""
number = int(input("input a number: "))

class Solution:

    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"
        thai_num = {0: "ศูนย์", 1: "หนึ่ง", 2: "สอง", 3: "สาม", 4: "สี่", 5: "ห้า",6: "หก", 7: "เจ็ด", 8: "แปด", 9: "เก้า", 10: "สิบ",
            20: "ยี่สิบ", 30: "สามสิบ", 40: "สี่สิบ", 50: "ห้าสิบ",60: "หกสิบ", 70: "เจ็ดสิบ", 80: "แปดสิบ", 90: "เก้าสิบ", 
            100: "ร้อย", 1000: "พัน", 10000: "หมื่น", 100000: "แสน", 1000000: "ล้าน"
        }
        if number == 0:
            return thai_num[0]
        result = []
        units = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
        
        num_str = str(number)[::-1]
        for i, digit in enumerate(num_str):
            if digit == '0':
                continue
            if i == 1 and digit == '1':
                result.append("สิบ")
            elif i == 1 and digit == '2':
                result.append("ยี่สิบ")
            else:
                result.append(thai_num[int(digit)] + units[i])
                
        return ''.join(result[::-1])

sol = Solution()
print(sol.number_to_thai(number))