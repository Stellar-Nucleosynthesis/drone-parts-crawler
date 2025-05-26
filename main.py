from website_parsers import generic_parser
from websites import fpvua
from persistence import object_save, db_save

def parse_marketplace(filename):
    parser = generic_parser.MarketplaceParser(fpvua.url, fpvua.detail_paths,
                                              fpvua.detail_url_finder, fpvua.attr_parsers, fpvua.normalizers)
    result = parser.parse()
    for detail, df in result.items():
        print("Detail:", detail)
        print(df.to_string(), '\n')
    object_save.save_to_pickle(result, filename)

def save_to_db(filename, dbname):
    scan_res = object_save.load_from_pickle(filename)
    for detail, df in scan_res.items():
        db_save.save_df_to_db(detail, df, dbname)


parse_marketplace("scan_results/scan_res.pickle")
save_to_db("scan_results/scan_res.pickle", "scan_results/database.db")
