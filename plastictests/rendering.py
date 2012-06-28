import json

from attest import Tests, assert_hook
from werkzeug.test import Client
from werkzeug.wrappers import Response

from plastic.app import BaseApp
from plastic.rendering import render


RenderingTestApp = BaseApp.clone()
RenderingTestApp.associate_mimetypes(html='text/html', xml='text/xml')


@RenderingTestApp.serializer('application/json')
def serialize_json(request, value):
    return json.dumps(value)


@RenderingTestApp.template_engine('t1')
def t1(request, path, values):
    with request.app.template_directory[path] as template:
        return template.read().format(request=request, **values)


@RenderingTestApp.route('/')
def home(request):
    return render(request, {'pi': 3.14}, 'home', pi=3.14)


tests = Tests()


@tests.test
def render_():
    client = Client(RenderingTestApp(), Response)
    response = client.get('/', headers=[('Accept', 'text/html')])
    assert response.data.strip() == '<h1>3.14</h1>'
    response = client.get('/', headers=[('Accept', 'text/xml')])
    assert response.data.strip() == '<pi value="3.14"/>'
    response = client.get('/', headers=[('Accept', 'application/json')])
    assert json.loads(response.data)['pi'] == 3.14
    response = client.get('/', headers=[('Accept', 'text/plain')])
    assert response.status_code == 406

