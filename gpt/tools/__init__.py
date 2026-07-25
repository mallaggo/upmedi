from .excel import EXCEL_TOOL, create_excel_file
from .product import SEARCH_PRODUCT_TOOL, search_product
from .email import EMAIL_TOOL, send_email

TOOL_SCHEMAS = [
    EXCEL_TOOL,
    SEARCH_PRODUCT_TOOL,
    EMAIL_TOOL,
]

TOOL_FUNCTIONS = {
    "create_excel_file": create_excel_file,
    "search_product": search_product,
    "send_email":send_email,
}