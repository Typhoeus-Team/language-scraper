import scrapy

from ..items import ConjugationItem
from ..verbs import spanishVerbs


class SpanishConjugationSpider(scrapy.Spider):
    name = "spanish"

    indicativeTenseRowDict = {
        "present": 3,
        "imperfect": 4,
        "preterite": 5,
        "future": 6,
        "conditional": 7,
    }

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

        # === Values: ===

        infinitive = conjugation_table.xpath(
            "./tr/th/span[text()='infinitive']/../../td/descendant-or-self::*/text()").get()

        # Indicative
        for tense in self.indicativeTenseRowDict:
            yield self.build_item(conjugation_header, infinitive, "indicative", tense)

    def build_urls(self):
        urls = []
        for verb in spanishVerbs.verbs:
            urls.append("https://en.wiktionary.org/wiki/" + verb)
        return urls

    def build_item(self, header, infinitive, mood, tense):
        row = header.xpath(
            "./../following-sibling::tr[$rowIndex]", rowIndex=self.indicativeTenseRowDict[tense])
        item = ConjugationItem()

        item['infinitive'] = infinitive
        item['mood'] = mood
        item['tense'] = tense

        # Might prove necessary to map out exact cell locations based on colspan values
        # of header rows. But so far, this seems sufficient.
        item['singular_first'] = row.xpath(
            "./td[1]/descendant-or-self::*/text()").get()
        item['singular_second'] = row.xpath(
            "./td[2]/descendant-or-self::*/text()").get()
        item['singular_third'] = row.xpath(
            "./td[3]/descendant-or-self::*/text()").get()

        item['plural_first'] = row.xpath(
            "./td[4]/descendant-or-self::*/text()").get()
        item['plural_second'] = row.xpath(
            "./td[5]/descendant-or-self::*/text()").get()
        item['plural_third'] = row.xpath(
            "./td[6]/descendant-or-self::*/text()").get()

        return item
