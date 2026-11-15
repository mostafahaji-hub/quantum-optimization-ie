# Chapter 5, code listing 1 (in order of appearance)
def is_good(code):           # code: '000' ... '111'
    if code not in code_table:       # 110 and 111 are not schedules
        return False
    return twt(code_table[code]) <= 8   # objective at most 8?