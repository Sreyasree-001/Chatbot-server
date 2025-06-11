# # import re
# # from rapidfuzz import fuzz
# # from database.extension import db
# # from database.models import Product

# # # Optional synonym logic for price adjectives
# # SYNONYMS = {
# #     "cheap": {"max_price": 50},
# #     "budget": {"max_price": 50},
# #     "expensive": {"min_price": 100},
# #     "premium": {"min_price": 150}
# # }


# # def get_categories():
# #     return [cat[0].lower() for cat in db.session.query(Product.category).distinct()]


# # def get_product_names():
# #     return [p[0].lower() for p in db.session.query(Product.name).all()]


# # def fuzzy_match_name(query, product_names):
# #     best_match = max(product_names, key=lambda name: fuzz.partial_ratio(query, name))
# #     return best_match if fuzz.partial_ratio(query, best_match) > 70 else None


# # def parse_query(query):
# #     query = query.lower()

# #     filters = {
# #         "category": None,
# #         "name": None,
# #         "min_price": None,
# #         "max_price": None
# #     }

# #     categories = get_categories()
# #     product_names = get_product_names()

# #     # Match known categories
# #     for cat in categories:
# #         if cat in query:
# #             filters["category"] = cat
# #             break

# #     # Match synonyms (cheap, premium, etc.)
# #     for key, value in SYNONYMS.items():
# #         if key in query:
# #             filters.update(value)

# #     # Match price: under, above, between
# #     if match := re.search(r"(under|below)\s*\$?(\d+\.?\d*)", query):
# #         filters["max_price"] = float(match.group(2))
# #     if match := re.search(r"(above|over|more than)\s*\$?(\d+\.?\d*)", query):
# #         filters["min_price"] = float(match.group(2))
# #     if match := re.search(r"between\s*\$?(\d+\.?\d*)\s*(and|-)\s*\$?(\d+\.?\d*)", query):
# #         filters["min_price"] = float(match.group(1))
# #         filters["max_price"] = float(match.group(3))

# #     # Fuzzy match product name
# #     tokens = query.split()
# #     for word in tokens:
# #         name_match = fuzzy_match_name(word, product_names)
# #         if name_match:
# #             filters["name"] = name_match
# #             break

# #     return filters
# from rapidfuzz import process

# CATEGORIES = [
#     "electronics", "groceries", "home goods", "furniture", "books",
#     "smart home", "sports & outdoors", "kitchenware", "fashion",
#     "musical instruments", "travel"
# ]

# def parse_query(query):
#     query = query.lower().strip()
#     filters = {}

#     # Price logic
#     price_keywords = {
#         "cheap": 50,
#         "under 100": 100,
#         "expensive": 300,
#         "premium": 300,
#         "budget": 75
#     }

#     for key, max_price in price_keywords.items():
#         if key in query:
#             filters['max_price'] = max_price
#             break

#     # 🔐 Safe fuzzy match
#     result = process.extractOne(query, CATEGORIES, score_cutoff=75)
#     if result:
#         matched_category, score, _ = result
#         filters['category'] = matched_category

#     return filters
import re
from rapidfuzz import process, fuzz

# Known categories in your DB
CATEGORIES = [
    "electronics", "groceries", "home goods", "furniture", "books",
    "smart home", "sports & outdoors", "kitchenware", "fashion",
    "musical instruments", "travel"
]

# Price-related keywords
SYNONYMS = {
    "cheap": {"max_price": 50},
    "budget": {"max_price": 75},
    "expensive": {"min_price": 300},
    "premium": {"min_price": 300}
}

# Simulated product names (replace with DB values)
PRODUCT_NAMES = [
    "electric toothbrush", "air fryer", "office chair",
    "guitar", "running shoes", "coffee maker", "refrigerator"
]


def parse_query(query):
    query = query.lower().strip()
    filters = {
        "category": None,
        "name": None,
        "min_price": None,
        "max_price": None
    }

    # Apply synonyms
    for key, price in SYNONYMS.items():
        if key in query:
            filters.update(price)
            break

    # Price range
    if match := re.search(r"(under|below)\s*\$?(\d+)", query):
        filters["max_price"] = float(match.group(2))
    elif match := re.search(r"(above|over|more than)\s*\$?(\d+)", query):
        filters["min_price"] = float(match.group(2))
    elif match := re.search(r"between\s*\$?(\d+)\s*(and|-)\s*\$?(\d+)", query):
        filters["min_price"] = float(match.group(1))
        filters["max_price"] = float(match.group(3))

    # Category match
    cat_match = process.extractOne(query, CATEGORIES, scorer=fuzz.partial_ratio, score_cutoff=70)
    if cat_match:
        filters["category"] = cat_match[0]

    # Product name match — only if not already matched as category
    if not filters["category"]:
        for token in query.split():
            prod_match = process.extractOne(token, PRODUCT_NAMES, scorer=fuzz.partial_ratio, score_cutoff=80)
            if prod_match:
                filters["name"] = prod_match[0]
                break

    return filters
