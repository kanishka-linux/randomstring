# RandomString

A simple random string generator using regular expression

# Installation

        pip install git+https://github.com/kanishka-linux/randomstring.git
        
# Documentation

        from randomstring import RandomString
        
        rstring = RandomString(10)
        
        regex = '[a-d][1-9]{4}|[e-f][4-7]{1,3}'
        
        rstring.generate_random_string(regex)
