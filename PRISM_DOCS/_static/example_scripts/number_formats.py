from math import pi

formatL = ['%s','%r','%f','%F','%g','%G','%e','%E']
numberL = [0.0, pi, 2.3, 1.23456E-8, 1.23456E8]

print '================================================'

for format in formatL: # loop through formats
        print format,
        for number in numberL: # loop through numbers
            s = format%number 
            print s.ljust(14),
        print
print '================================================'

specL = ['','.','.3','.2','#','#.']

for format in formatL: # loop through formats
    for spec in specL: # loop through special characters in formats
        fmt = format[0] + spec + format[1:] # build special format
        print fmt.ljust(4),
        for number in numberL: # loop through numbers
            s = fmt%number 
            if s.strip() == '':
                s = '###'
            print s.ljust(13),
        print
    print
        