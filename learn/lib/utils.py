def formatPath(string):
    """Formats a string for integration into a url path"""
    return string.replace(' ', '_')

def pathToString(string):
    """Formats a path to a user-friendly string"""
    return string.replace('_', ' ')