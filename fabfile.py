import os

from os.path import join, abspath, dirname

from fabric.api import local, task, env, settings, hide, lcd
from fabric.colors import green, red
from fabric.utils import abort

env.project = 'weckan'

ROOT = abspath(join(dirname(__file__)))


#######################################################################################################################
#                                               Development tasks                                                     #
#######################################################################################################################
@task
def mig(app='webnotes'):
    '''
    Generate a south migration for an application
    '''
    with lcd(ROOT):
        local('python manage.py schemamigration "%s" --auto' % app)


@task
def datamig(app, name):
    '''
    Generate a south data migration for an application
    '''
    with lcd(ROOT):
        local('python manage.py datamigration "%s" "%s"' % (app, name))


@task
def syncdb():
    '''
    Synchronize database and generate changesets
    '''
    with lcd(ROOT):
        local('python manage.py syncdb --noinput')
        local('python manage.py migrate --noinput')


@task
def init():
    '''
    Initialize database and user.
    '''
    syncdb()
    with lcd(ROOT):
        local('python manage.py createsuperuser')


@task
def serve(port=8000):
    '''
    Run Development server.
    '''
    with lcd(ROOT):
        local('python manage.py runserver %s' % port)


def get_apps(app=None, canonical=False):
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from weckan.settings import PROJECT_APPS

    apps = [app] if app else PROJECT_APPS
    return apps if canonical else [a.split('.')[-1] for a in apps]


@task
def test(app=None, verbose=False):
    '''
    Run only project tests (exclude those from Django and third-party applications).
    '''
    apps = ' '.join(get_apps(app))
    verbosity = 2 if verbose else 1
    with settings(warn_only=True), hide('warnings'):
        with lcd(ROOT):
            result = local('python manage.py test %s --verbosity=%s' % (apps, verbosity))
        if result.failed:
            print(red('Some tests failed !!'))
            abort('Tests failed')
        else:
            print(green("All tests passed. Yeah!"))


@task
def coverage(app=None):
    '''Run the test suite with coverage'''
    apps = ' '.join(get_apps(app))
    local('coverage erase')
    local('coverage run --rcfile=coverage.rc manage.py test {}'.format(apps))
    local('coverage report --rcfile=coverage.rc')


@task
def pep8(app=None):
    '''Run the PEP8 report'''
    local('pep8 --rcfile=pep8.rc')
    print('PEP8: OK')


@task
def pylint(app=None):
    '''Run the pylint report'''
    local('pylint --rcfile=pylint.rc weckan')


@task
def test_all():
    '''
    Run all tests (including those from Django and third-party applications).
    '''
    with lcd(ROOT):
        local('python manage.py test')


@task
def doc():
    '''
    Generate the documentation.
    '''
    with lcd(join(ROOT, 'doc')):
        local('make html')


@task
def update_dependencies():
    '''
    Update to last dependencies version.
    '''
    with lcd(ROOT):
        local('pip install -q -r requirements/tools.pip')
        local('pip install -q -r requirements/install.pip')
        local('pip install -q -r requirements/develop.pip')


@task
def update_js():
    '''
    Update javascript dependencies
    '''
    # local('npm install')
    with lcd(ROOT):
        local('bower install')


@task
def update():
    '''
    Update all dependencies and database
    '''
    update_dependencies()
    update_js()
    syncdb()


@task
def make_messages(lang=None):
    '''
    Generate translation files (.mo)
    '''
    lang = '-l %s' % lang if lang else '-a'
    with lcd(join(ROOT, 'weckan')):
        local('django-admin.py makemessages %s' % lang)
    local('python manage.py js localize weckan %s --ignore=static/bower/*' % lang)


@task
def compile_messages():
    '''
    Compile translation files (.po)
    '''
    with lcd(join(ROOT, 'weckan')):
        local('django-admin.py compilemessages')


@task
def sdist(buildno=None):
    '''
    Build a source distribution
    '''
    with lcd(ROOT):
        local('python setup.py clean')
        local('rm -rf *egg-info build dist')
        if buildno:
            local('python setup.py -q egg_info -b ".%s" sdist' % buildno)
        else:
            local('python setup.py -q sdist')
