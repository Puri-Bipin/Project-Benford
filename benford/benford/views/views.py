import csv
import io
from pyramid.view import view_config
from pyramid.response import Response
import json
from math import log10


@view_config(route_name='benford', request_method='POST')
def benford(request):
    # Get the uploaded file from the request
    file = request.POST['file'].file

    # Determine the encoding of the uploaded file
    content_type = request.POST['file'].headers.get('Content-Type')
    charset = content_type.split('charset=')[-1] if content_type else 'utf-8'

    # Read the CSV file and extract the first digits
    first_digits = []
    for line in csv.reader(io.TextIOWrapper(file, encoding='utf-8')):
        # Skip the header line
        if line[0].isdigit():
            first_digits.append(int(line[0][0]))

    # Calculate the expected distribution of first digits according to Benford's law
    expected_distribution = {i: log10(1 + 1/i) * 100 for i in range(1, 10)}

    # Calculate the actual distribution of first digits in the input file
    actual_distribution = {i: first_digits.count(i) / len(first_digits) * 100 for i in range(1, 10)}

    # Compare the actual and expected distributions and determine if the input conforms to Benford's law
    is_conforming = all(abs(expected_distribution[i] - actual_distribution[i]) < 1 for i in range(1, 10))

    # Prepare the JSON response
    response_data = {
        'is_conforming': is_conforming,
        'expected_distribution': expected_distribution,
        'actual_distribution': actual_distribution
    }

    return Response(json.dumps(response_data), content_type='application/json; charset=utf-8')

