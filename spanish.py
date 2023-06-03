import scrapy


class SpanishConjugationSpider(scrapy.Spider):
    name = "spanish_conjugation"

    # TODO: However we want to actually source a list of verbs
    verbs = [
        "jugar",
        "hacer",
        "tomar",
        "decir",
        "mirar",
        "trabajar",
        "poder",
        "vivar",
        "llegar",
        "volver",
        "estudiar",
        "tener",
        "poner",
        "saber",
        "salir",
    ]

    def start_requests(self):
        urls = self.build_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # === Queries: ===
        conjugation_table = response.xpath(
            "//h2/span[text()='Spanish']/following::h4/span[text()='Conjugation']/following::table[1]/tbody")

        conjugation_header = conjugation_table.xpath(
            "./tr/th[translate(text(), '\n', '')='singular' and @colspan='3']")

        present_row = conjugation_header.xpath("./../following-sibling::tr[3]")

        preterite_row = conjugation_header.xpath(
            "./../following-sibling::tr[5]")

        # === Values: ===
        infinitive = conjugation_table.xpath(
            "./tr/th/span[text()='infinitive']/../../td/descendant-or-self::*/text()").get()

        # TODO: Could clean all of this up by moving things into "Items". As is, this file would
        # grow MASSIVE.

        # Could make this selection more robust by mapping out the colspan values of the header.
        # But that seems like a lot of work if not absolutely necessary.
        singular_first = present_row.xpath(
            "./td[1]/descendant-or-self::*/text()").get()
        singular_second = present_row.xpath(
            "./td[2]/descendant-or-self::*/text()").get()
        singular_third = present_row.xpath(
            "./td[3]/descendant-or-self::*/text()").get()

        plural_first = present_row.xpath(
            "./td[4]/descendant-or-self::*/text()").get()
        plural_second = present_row.xpath(
            "./td[5]/descendant-or-self::*/text()").get()
        plural_third = present_row.xpath(
            "./td[6]/descendant-or-self::*/text()").get()

        yield {
            "infinitive": infinitive,
            "mood": "indicative",
            "tense": "present",
            "singular_first": singular_first,
            "singular_second": singular_second,
            "singular_third": singular_third,
            "plural_first": plural_first,
            "plural_second": plural_second,
            "plural_third": plural_third,
        }

        singular_first = preterite_row.xpath(
            "./td[1]/descendant-or-self::*/text()").get()
        singular_second = preterite_row.xpath(
            "./td[2]/descendant-or-self::*/text()").get()
        singular_third = preterite_row.xpath(
            "./td[3]/descendant-or-self::*/text()").get()

        plural_first = preterite_row.xpath(
            "./td[4]/descendant-or-self::*/text()").get()
        plural_second = preterite_row.xpath(
            "./td[5]/descendant-or-self::*/text()").get()
        plural_third = preterite_row.xpath(
            "./td[6]/descendant-or-self::*/text()").get()

        yield {
            "infinitive": infinitive,
            "mood": "indicative",
            "tense": "preterite",
            "singular_first": singular_first,
            "singular_second": singular_second,
            "singular_third": singular_third,
            "plural_first": plural_first,
            "plural_second": plural_second,
            "plural_third": plural_third,
        }

    def build_urls(self):
        urls = []
        for verb in self.verbs:
            urls.append("https://en.wiktionary.org/wiki/" + verb)
        return urls
