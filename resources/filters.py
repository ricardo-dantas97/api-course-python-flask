def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=100000, limit=50, offset=0, **data):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset,
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset,
    }


query_without_city = """
    SELECT *
    FROM hoteis
    WHERE (estrelas >= ? AND estrelas <= ?)
    AND (diaria >= ? AND diaria <= ?)
    LIMIT ?
    OFFSET ?
"""

query_with_city = """
    SELECT *
    FROM hoteis
    WHERE (estrelas >= ? AND estrelas <= ?)
    AND (diaria >= ? AND diaria <= ?)
    AND cidade = ?
    LIMIT ?
    OFFSET ?
"""


