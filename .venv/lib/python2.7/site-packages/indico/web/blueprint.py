from __future__ import absolute_import, unicode_literals

import json

from flask import request
from werkzeug.exceptions import Forbidden, NotFound
from wtforms import BooleanField, StringField

from indico.core.errors import UserValueError
from indico.web.flask.wrappers import IndicoBlueprint
from indico.web.forms.base import IndicoForm
from indico.web.rh import RH, RHSimple
from indico.web.util import jsonify_data, jsonify_form
from indico.web.views import WPDecorated, WPJinjaMixin


testbp = IndicoBlueprint('test', __name__)


class WPTest(WPJinjaMixin, WPDecorated):
    def _getBody(self, params):
        return WPJinjaMixin._getPageContent(self, params).encode('utf-8')


def _send_email(with_event):
    from flask import session
    from indico.core.notifications import send_email, make_email
    from indico.modules.events import Event
    from indico.modules.users import User
    from indico.web.flask.templating import get_template_module
    tpl = get_template_module('users/emails/registration_request_accepted.txt', user=User.get(6))
    kwargs = {}
    if with_event:
        kwargs = {'event': Event.get(654658), 'module': 'Test', 'user': session.user}
    # send_email(make_email('m\xf6p@example.com', template=tpl), **kwargs)
    # send_email(make_email('moep@example.com', template=tpl), **kwargs)
    from indico.modules.events.registration.notifications import _notify_registration
    from indico.modules.events.registration.models.registrations import Registration
    _notify_registration(Registration.get(56757), 'registration_creation_to_registrant.html')


class RHTest(RH):
    CSRF_ENABLED = False

    def _process(self):
        dialog = request.args.get('dialog') == '1'
        form = TestForm(prefix='dlg-' if dialog else '', csrf_enabled=False)
        data = {}
        if form.validate_on_submit():
            _send_email(form.with_event.data)
            data = form.data
        elif form.is_submitted():
            data = form.errors
        if dialog:
            if form.validate_on_submit():
                if form.check.data:
                    raise ValueError('You are full of fail (or ValueErrors)')
                if form.check2.data:
                    raise UserValueError('You sent us failing garbage')
                if form.check3.data:
                    raise Forbidden('You shall not pass')
                if form.check4.data:
                    raise NotFound('Keep going, nothing to see here...')
                return jsonify_data(flash=False, html=json.dumps(data))
            return jsonify_form(form)
            # return jsonify_form(form, form_header_kwargs={'action': '/robots.txt'})
        else:
            return WPTest.render_template('test.html', form=form, data=data)


class TestForm(IndicoForm):
    text = StringField('Text')
    with_event = BooleanField('With event', default=True)
    check = BooleanField('Fail')
    check2 = BooleanField('Fail (noreport)')
    check3 = BooleanField('Fail (forbidden)')
    check4 = BooleanField('Fail (notfound)')


testbp.add_url_rule('/test/', 'test', RHTest, methods=('GET', 'POST'))


@testbp.route('/logit')
def logit():
    import logging
    from indico.core.logger import Logger
    Logger.get('foo').debug('this is debug')
    Logger.get('foo').info('this is info')
    Logger.get('foo').warning('this is warning')
    Logger.get('foo').error('this is error')
    logging.getLogger('foobar').debug('this is OTHER debug')
    logging.getLogger('foobar').info('this is OTHER info')
    logging.getLogger('foobar').warning('this is OTHER warning')
    logging.getLogger('foobar').error('this is OTHER error')
    logging.getLogger('celery.dummy').debug('this is CELERY debug')
    logging.getLogger('celery.dummy').info('this is CELERY info')
    logging.getLogger('celery.dummy').warning('this is CELERY warning')
    logging.getLogger('celery.dummy').error('this is CELERY error')
    return 'meow'


@testbp.route('/test2')
@RHSimple.wrap_function
def test2():
    from werkzeug.exceptions import Forbidden
    from indico.modules.auth.util import redirect_to_login
    raise Forbidden(response=redirect_to_login(reason='YOU SHALL NOT PASS WITHOUT LOGGING IN'))


@testbp.route('/notfound')
def test3():
    from werkzeug.exceptions import NotFound
    raise NotFound('user brain not found')


@testbp.route('/badrequest')
def test4():
    from werkzeug.exceptions import BadRequest
    raise BadRequest('your requests suck')


@testbp.route('/badrequestkey')
def test5():
    from flask import request
    request.form['foo']


@testbp.route('/unauth')
def test6():
    from werkzeug.exceptions import Unauthorized
    raise Unauthorized('you shall authorize')


@testbp.route('/badmethod')
def test7():
    from werkzeug.exceptions import MethodNotAllowed
    raise MethodNotAllowed('your methods suck')


@testbp.route('/unavailable')
def test8():
    from werkzeug.exceptions import ServiceUnavailable
    raise ServiceUnavailable('we do not serve your kind here')


@testbp.route('/badsig')
def test9():
    from itsdangerous import BadSignature
    raise BadSignature('your data smells')


@testbp.route('/general')
def test10():
    from indico.core.errors import IndicoError
    raise IndicoError('your indicoes are on fire')


@testbp.route('/noreport')
def test11():
    from indico.core.errors import NoReportError
    raise NoReportError('we do not care about your error')


@testbp.route('/uservalue')
def test12():
    from indico.core.errors import UserValueError
    raise UserValueError('your values suck')


@testbp.route('/noresult')
def test13():
    from werkzeug.exceptions import NotFound
    raise NotFound('The specified item could not be found.')
