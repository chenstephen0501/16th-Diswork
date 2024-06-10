from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(queryset, page_number, per_page=5):
    paginator = Paginator(queryset, per_page)
    try:
        page_obj = paginator.page(page_number)
        is_paginated = paginator.num_pages > 1
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
        is_paginated = False 
    return page_obj, is_paginated