import scrapy

from ..items import ConjugationItem
from ..items import ParticipleItem
from ..verbs import frenchVerbs


class FrenchConjugationSpider(scrapy.Spider):
    name = "french"

    indicativeTenseRowDict = {
        "present": 1,
        "imperfect": 2,
        "preterite": 3,
        "future": 4,
        "conditional": 5,
    }

    def start_requests(self):
        urls = self.build_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # === Queries: ===
        conjugation_table = response.xpath(
            "//h2/span[text()='French']/following::h4/span[text()='Conjugation']/following::table[1]/tbody")[0]

        conjugation_indicative_header = conjugation_table.xpath(
            "./tr/th/span[contains (text(), 'indicative')]")

        infinitive = conjugation_table.xpath(
            "./tr/th/span[contains (text(), 'infinitive')]/following::td[1]/text()").get().strip()

        # yield self.build_participle_item(conjugation_table, infinitive)

        # Indicative
        for tense in self.indicativeTenseRowDict:
            yield self.build_conjugation_item(conjugation_indicative_header, infinitive, "indicative", tense)
        # yield self.build_conjugation_item(conjugation_indicative_header, infinitive, "indicative", "present")

    def build_urls(self):
        urls = []
        for verb in frenchVerbs.verbs:
            urls.append("https://en.wiktionary.org/wiki/" + verb)
        return urls

    def build_participle_item(self, conjugation_table, infinitive):
        item = ParticipleItem()

        item['infinitive'] = infinitive
        
        # In some cases two pronunciations are given, just take the first. Find a better way to do this
        item['present_participle'], item['present_participle_pronunciation'] = conjugation_table.xpath(
            "./tr/th/span[contains (text(), 'present participle')]/following::td[1]/span/descendant-or-self::*/text()").getall()[:2]
        
        item['past_participle'], item['past_participle_pronunciation'] = conjugation_table.xpath(
            "./tr/th/span[contains (text(), 'past participle')]/following::td[1]/span/descendant-or-self::*/text()").getall()[:2]

        return item

    def build_conjugation_item(self, header, infinitive, mood, tense):
        row = header.xpath(
            "./../../following-sibling::tr[$rowIndex]", rowIndex=self.indicativeTenseRowDict[tense])
        item = ConjugationItem()

        item['infinitive'] = infinitive
        item['mood'] = mood
        item['tense'] = tense

        # Might prove necessary to map out exact cell locations based on colspan values
        # of header rows. But so far, this seems sufficient.
        item['singular_first'] = row.xpath(
            "./td[1]/span[1]/descendant-or-self::*/text()").get()
        item['singular_second'] = row.xpath(
            "./td[2]/span[1]/descendant-or-self::*/text()").get()
        item['singular_third'] = row.xpath(
            "./td[3]/span[1]/descendant-or-self::*/text()").get()

        item['plural_first'] = row.xpath(
            "./td[4]/span[1]/descendant-or-self::*/text()").get()
        item['plural_second'] = row.xpath(
            "./td[5]/span[1]/descendant-or-self::*/text()").get()
        item['plural_third'] = row.xpath(
            "./td[6]/span[1]/descendant-or-self::*/text()").get()

        return item
