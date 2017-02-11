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
