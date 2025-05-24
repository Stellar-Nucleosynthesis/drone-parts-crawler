from website_parsers import generic_parser
from websites import fpvua

parser = generic_parser.MarketplaceParser(fpvua.url, fpvua.detail_paths,
                                          fpvua.detail_url_finder, fpvua.attr_parsers)
result = parser.parse()
for detail, df in result.items():
    print("Detail:", detail)
    print(df.to_string(), '\n')