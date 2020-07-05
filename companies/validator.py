
import re


class Validator:
    @classmethod
    def is_valid_company_id(cls, companyId):

        # Old form has 6 numbers, zero needs to be added in front in this case
        matchOldForm = re.search("\\A[0-9]{6}\\-[0-9]{1}", companyId)
        if matchOldForm:
            # Add zero
            companyId = "0"+companyId

        match = re.search("\\A[0-9]{7}\\-[0-9]{1}", companyId)
        if match:
            # Validate checksum of business ID
            numbers = [int(char) for char in companyId[:7]]
            multipliers = [7, 9, 10, 5, 8, 4, 2]
            result = 0
            index = 0
            for number in numbers:
                result += number*multipliers[index]
                index = index + 1

            remainder = result % 11
            if remainder == 0:
                # Checksum should be 0
                checksum = 0
            else:
                checksum = 11-remainder

            if int(companyId[8]) == checksum:
                return True
            else:
                return False
        return False
