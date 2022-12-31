import re

def parse_checkboxes(request: object) -> list:
    """
    parse the body of the form containing a table with checkboxes and return list of checkboxes names
    """
    request_body = request.body.decode('ascii')
    raw = request_body[request_body.find('&'):]
    filter_start = re.finditer(pattern='&', string=raw)
    filter_stop = re.finditer(pattern='=', string=raw)
    indices_start = [index.start() for index in filter_start]
    indices_stop = [index.start() for index in filter_stop]
    boxes = [raw[start + 1:stop] for start, stop in zip(indices_start, indices_stop)]
    return boxes