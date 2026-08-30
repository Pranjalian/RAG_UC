"""
Mappings to group raw scraper fields into logical normalized sections.
"""

SECTION_MAPPINGS = {
    "overview": [
        "scheme_name",
        "groww_rating",
        "crisil_rating",
        "category",
        "sub_category",
        "description",
        "benchmark_name",
        "launch_date",
        "aum",
        "expense_ratio",
        "min_sip_investment",
        "min_investment_amount",
        "exit_load",
        "stamp_duty",
        "nav",
        "nav_date"
    ],
    "returns": [
        "return_stats",
        "sip_return",
        "simple_return"
    ],
    "fund_managers": [
        "fund_manager_details"
    ],
    "amc_details": [
        "amc_info"
    ],
    "holdings": [
        "holdings"
    ]
}
