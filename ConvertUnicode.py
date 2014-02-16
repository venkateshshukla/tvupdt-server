import imdb

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8', 'replace')
    elif isinstance(input, imdb.Person.Person):
        return convert(input.data)
    elif isinstance(input, imdb.Company.Company):
        return convert(input.data)
    elif isinstance(input, imdb.Movie.Movie):
        return convert(input.data)
    else:
        return input
