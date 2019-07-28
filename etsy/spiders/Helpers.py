import scrapy


class Helpers:

    @staticmethod
    def parse(response, list_of_css, default):

        out = default

        for css in list_of_css:
            val = response.css(css).extract()
            if len(val) != 0:
                break

        if len(val) != 0:
            out = val[0]

        return out



def letterify(a,b,c):
    base = ord('a')
    return chr(a+base) + chr(b + base) + chr(c + base)

def give_me_3():
    for a in range(0,26):
        for b in range(0,26):
            for c in range(0,26):
                yield letterify(a,b,c)
