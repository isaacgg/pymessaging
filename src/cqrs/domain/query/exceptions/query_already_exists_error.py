class QueryAlreadyExistsError(Exception):
    def __init__(self, query_name):
        self.message = f'Unable to register query. {query_name} already exist'
        super(QueryAlreadyExistsError, self).__init__()
