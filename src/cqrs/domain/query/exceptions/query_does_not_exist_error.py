class QueryDoesNotExistError(Exception):
    def __init__(self, query_name):
        self.message = f'Unable to execute query. {query_name} does not exist'
        super(QueryDoesNotExistError, self).__init__()
