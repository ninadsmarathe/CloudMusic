class Solution(object):
    def numberToWords(self, num):
        """
        :type num: int
        :rtype: str
        """
        without_trim = ""
        final_ans = ""
        units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        teens = ['', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen',
                 'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy',
                'Eighty', 'Ninety']
        thousands = ['', 'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion',
                     'Quintillion', 'Sextillion', 'Septillion', 'Octillion',
                     'Nonillion', 'Decillion', 'Undecillion', 'Duodecillion',
                     'Tredecillion', 'Quattuordecillion', 'Sexdecillion',
                     'Septendecillion', 'Octodecillion', 'Novemdecillion',
                     'Vigintillion']

        def hundred_number(n):
            if 99 < int(n) < 1000 and int(n) % 100 != 0:
                return hundred_number(int(n) - int(n) % 100) + " " + tens_number(int(n) % 100)

            if 99 < int(n) < 999 and int(n) % 100 == 0:
                return unit_number(int(int(n) / 100)) + " Hundred"

        def tens_number(n):

            if 20 < int(n) < 100 and int(n) % 10 != 0:
                return tens_number(int(n) - int(n) % 10) + " " + unit_number(int(n) % 10)
            elif 10 < int(n) < 20:
                return teens[int(int(n) % 10)]
            elif 9 < int(n) < 99 and int(n) % 10 == 0:
                return tens[int(int(n) / 10)]
            elif int(n) > 0:
                return unit_number(n)

        def unit_number(n):
            return units[int(n)]

        def three_digit_number(n):
            if int(n) == 0:
                return ''
            elif 99 < int(n) < 1000:
                return hundred_number(int(n))

            elif 9 < int(n) < 100:
                return tens_number(int(n))

            elif int(n) > 0:
                return unit_number(int(n))

        def divide_into_three(s):
            i = 0
            q = str(s)
            list_ = []
            count = 0
            s = ""
            # v=len(str(q)) // 3
            for j in range(int(len(q) / 3)):
                if int(len(q) / 3) >= 1:
                    s = s + q[-3 + i] + q[-2 + i] + q[-1 + i]
                    i = i - 3
                    list_.append(s)
                    s = ""
                    count = i

            if len(q) % 3 != 0:
                list_.append(q[:count])
            return list_

        final_list = divide_into_three(num)
        if num == 0:
            return 'Zero'
        elif num < 1000:
            return three_digit_number(num)
        else:
            for i in range(len(final_list)):
                if final_list[i] == '000':
                    final_ans = three_digit_number(int(final_list[i])) + " " + final_ans
                else:
                    final_ans = three_digit_number(int(final_list[i])) + " " + thousands[i] + " " + final_ans
            without_trim = final_ans
            sentence = without_trim
            return " ".join(sentence.split())


s=Solution()
print(s.numberToWords(1000000))