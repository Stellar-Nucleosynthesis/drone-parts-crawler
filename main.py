from details_parsing import details_parser
from details_parsing.websites import fpvua as fpvua_det
from distributors_parsing import distributor_parser
from distributors_parsing.websites import fpvua as fpvua_dist
from persistence import object_save, db_save

def parse_details(module):
    parser = details_parser.DetailsParser(module.url, module.detail_paths,
                                          module.detail_url_finder, module.attr_parsers,
                                          module.normalizers)
    result = parser.parse()
    for detail, df in result.items():
        print("Detail:", detail)
        print(df.to_string(), '\n')
    object_save.save_to_pickle(result, "scan_results/scan_res.pickle")

def load_details_dfs():
    return object_save.load_from_pickle("scan_results/scan_res.pickle")

def save_details_dfs(details_dfs):
    db_save.update_details_in_db("scan_results/database.db", details_dfs)

def parse_distributors(module, details_dfs):
    dist_parser = distributor_parser.DistributorsParser(
        module.search_detail, module.find_product_name, module.find_sale_info)
    res = dist_parser.parse(details_dfs)
    object_save.save_to_pickle(res, "scan_results/distributors.pickle")

def load_distributors_dfs():
    return object_save.load_from_pickle("scan_results/distributors.pickle")

def save_distributors_dfs(distributors_dfs):
    db_save.insert_distributor_info("scan_results/database.db", distributors_dfs)


parse_details(fpvua_det)
details = load_details_dfs()
parse_distributors(fpvua_dist, details)
distributors = load_distributors_dfs()

db_save.update_details_in_db("scan_results/database.db", details)
db_save.insert_distributor_info("scan_results/database.db", distributors)