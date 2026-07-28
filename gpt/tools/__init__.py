from .excel import EXCEL_TOOL, create_excel_file
from .product import SEARCH_PRODUCT_TOOL, search_product, read_excel_products, READ_EXCEL_PRODUCTS_TOOL
from .email import EMAIL_TOOL, send_email
from .save_products import save_products,SAVE_PRODUCTS_TOOL

TOOL_SCHEMAS = [
    EXCEL_TOOL,
    SEARCH_PRODUCT_TOOL,
    READ_EXCEL_PRODUCTS_TOOL,
    SAVE_PRODUCTS_TOOL,
    EMAIL_TOOL,
]

TOOL_FUNCTIONS = {
    "read_excel_products": read_excel_products,
    "create_excel_file": create_excel_file,
    "search_product": search_product,
    "save_products": save_products,
    "send_email":send_email,

}