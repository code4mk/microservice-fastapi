from urllib.parse import urlparse
from fastapi import Request

def paginate(request: Request, query, serilizer, the_page: int = 1, the_per_page: int = 10, wrap='data'):
    """Paginate the query."""
    
    page = int(request.query_params.get('page', the_page))
    per_page = int(request.query_params.get('per_page', the_per_page))
    
    total = query.count()
    last_page = (total + per_page - 1) // per_page
    offset = (page - 1) * per_page
    paginated_query = query.offset(offset).limit(per_page).all()

    data = [serilizer.from_orm(item) for item in paginated_query]

    base_url = str(request.base_url)
    
    full_path = str(request.url)
    parsed_url = urlparse(full_path)
    path_without_query = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    
    first_page_url = f"{path_without_query}?page=1&per_page={per_page}"
    last_page_url = f"{path_without_query}?page={last_page}&per_page={per_page}"
    next_page_url = f"{path_without_query}?page={page + 1}&per_page={per_page}" if page < last_page else None
    prev_page_url = f"{path_without_query}?page={page - 1}&per_page={per_page}" if page > 1 else None

    return {
        'total': total,
        'per_page': per_page,
        'current_page': page,
        'last_page': last_page,
        'first_page_url': first_page_url,
        'last_page_url': last_page_url,
        'next_page_url': next_page_url,
        'prev_page_url': prev_page_url,
        'path': base_url,
        'from': offset + 1 if data else None,
        'to': offset + len(data) if data else None,
        wrap: data
    }
