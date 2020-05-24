# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class ZooplaSpider(scrapy.Spider):
    name = 'zoopla'
    allowed_domains = ['zoopla.co.uk']
    start_urls = [
            'https://www.zoopla.co.uk/for-sale/houses/sr2/?beds_min=2&price_max=160000&identifier=sr2&property_type=houses&q=SR2&search_source=home&radius=0&pn=1',
            'https://www.zoopla.co.uk/for-sale/houses/ne4/?beds_min=2&price_max=160000&identifier=ne4&property_type=houses&q=NE4&search_source=home&radius=0&pn=1',
    ]

    def parse(self, response):
        for listing in response.css("div.listing-results-wrapper"):
            yield {
                'id': listing.css("::attr(data-listing-id)").extract_first(),
                'price': listing.css("a.text-price::text").extract_first().strip(),
                'title': listing.css("h2.listing-results-attr > a::text").extract_first(),
                'location': listing.css("a.listing-results-address::text").extract_first(),
                'url': ('https://www.zoopla.co.uk' + listing.css("a.photo-hover::attr(href)").extract_first()),
                'list-date': listing.css("p.listing-results-marketed > small::text").extract_first().strip()[11:-2].strip(),
                'realtor': listing.css("p.listing-results-marketed > span::text").extract_first(),
                'beds': listing.css("h3.listing-results-attr > span.num-beds::text").extract_first(),
                'receptions': listing.css("h3.listing-results-attr > span.num-reception::text").extract_first(),
                'description': listing.css('div.listing-results-right > p::text').extract_first().strip(),
            }

        next_page_url = response.css("div.paginate > a::attr(href)").extract()[-1]
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
