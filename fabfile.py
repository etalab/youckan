import os

from os.path import join, abspath, dirname

from fabric.api import local, task, env, settings, hide, lcd
from fabric.context_managers import shell_env
from fabric.colors import green, red
from fabric.utils import abort

env.project = 'youckan'

ROOT = abspath(join(dirname(__file__)))


#######################################################################################################################
#                                               Development tasks                                                     #
#######################################################################################################################
@task
def mig(app='youckan'):
    '''Generate a south migration for an application'''
    with lcd(ROOT):
        local('python manage.py schemamigration "%s" --auto' % app)


@task
def datamig(app, name):
    '''Generate a south data migration for an application'''
    with lcd(ROOT):
        local('python manage.py datamigration "%s" "%s"' % (app, name))


@task
def syncdb():
    '''Synchronize database and generate changesets'''
    with lcd(ROOT):
        local('python manage.py syncdb --noinput')
        local('python manage.py migrate --noinput')


@task
def init():
    '''Initialize database and user.'''
    syncdb()
    with lcd(ROOT):
        local('python manage.py createsuperuser')


@task
def serve(port=8000):
    '''Run Development server.'''
    with lcd(ROOT):
        local('python manage.py runserver %s' % port)


@task
def sso(port=8000):
    '''Run Development server.'''
    with lcd(ROOT), shell_env(DJANGO_SETTINGS_MODULE='youckan.auth.settings'):
        local('python manage.py runserver %s' % port)


@task
def work():
    '''Run the development worker'''
    with lcd(ROOT):
        local('python manage.py celery worker')

@task
def debug(port=8000):
    '''Run Development server.'''
    with lcd(ROOT):
        local('ipython --pdb manage.py runserver %s' % port)


def get_apps(app=None, canonical=False):
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from youckan.settings import PROJECT_APPS

    apps = [app] if app else PROJECT_APPS
    return apps if canonical else [a.split('.')[-1] for a in apps]


@task
def test(app=None, verbose=False):
    '''Run only project tests (exclude those from Django and third-party applications).'''
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
    local('pep8 --config=pep8.rc youckan')
    print('PEP8: OK')


@task
def pylint(app=None):
    '''Run the pylint report'''
    local('pylint --rcfile=pylint.rc -f colorized --reports=no youckan')


@task
def test_all():
    '''
    Run all tests (including those from Django and third-party applications).
    '''
    with lcd(ROOT):
        local('python manage.py test')


@task
def doc():
    '''Generate the documentation.'''
    with lcd(join(ROOT, 'doc')):
        local('make html')


@task
def update_py():
    '''Update python dependencies.'''
    with lcd(ROOT):
        local('pip install -q -r requirements/all.pip')


@task
def update_js():
    '''Update javascript dependencies'''
    # local('npm install')
    with lcd(ROOT):
        local('bower install')


@task
def update():
    '''Update all dependencies and database'''
    update_py()
    update_js()
    syncdb()


@task
def i18n(lang=None):
    '''Generate translation files (.mo)'''
    lang = '-l %s' % lang if lang else '-a'
    with lcd(join(ROOT, 'youckan')):
        local('django-admin.py makemessages %s' % lang)
    local('python manage.py js localize youckan %s --ignore=static/bower/*' % lang)


@task
def i18n_build():
    '''Compile translation files (.po)'''
    with lcd(join(ROOT, 'youckan')):
        local('django-admin.py compilemessages')


@task
def dist(buildno=None):
    '''Build a source distribution'''
    update_js()
    i18n_build()
    with lcd(ROOT):
        local('python setup.py clean')
        local('rm -rf *egg-info build dist')
        if buildno:
            local('python setup.py -q egg_info -b ".%s" sdist' % buildno)
        else:
            local('python setup.py -q sdist')

@task
def gdist():
    '''Build a source distribution with git version'''
    with lcd(ROOT):
        sha1 = local('git rev-parse --short HEAD', capture=True)
        dist(sha1)
