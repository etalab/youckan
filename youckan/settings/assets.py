# -*- coding: utf-8 -*-
from os.path import join, expanduser, expandvars

from youckan.settings.common import PACKAGE_ROOT, conf

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = expandvars(expanduser(conf['path']['media']))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = conf['path']['media_url']

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = expandvars(expanduser(conf['path']['static']))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = conf['path']['static_url']

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ('fonts', join(PACKAGE_ROOT, 'static', 'bower', 'bootstrap', 'fonts')),
    ('fonts', join(PACKAGE_ROOT, 'static', 'bower', 'etalab-assets', 'fonts')),
    ('images', join(PACKAGE_ROOT, 'static', 'bower', 'etalab-assets', 'img')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

LESS_INCLUDE_PATHS = (
    'bower/etalab-assets/less',
    'bower/bootstrap/less',
)

_less_include_path = (join(PACKAGE_ROOT, 'static', path) for path in LESS_INCLUDE_PATHS)
PIPELINE_LESS_ARGUMENTS = '--include-path=%s' % ':'.join(_less_include_path)

# PIPELINE_CSS_COMPRESSOR = 'webnotes.compressors.CSSMinCompressor'

PIPELINE_CSS = {
    'youckan': {
        'source_filenames': (
            'less/youckan.less',
        ),
        'output_filename': 'css/youckan.min.css',
    },
}

# PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_JS = {
    'modernizr': {
        'source_filenames': (
            'bower/modernizr/modernizr.js',
            'bower/respond/respond.src.js',
        ),
        'output_filename': 'js/modernizr.min.js',
    },
    'jquery': {
        'source_filenames': {
            'bower/jquery/jquery.js',
        },
        'output_filename': 'js/jquery.min.js',
    },
    'jquery-legacy': {
        'source_filenames': {
            'bower/jquery-legacy/index.js',
        },
        'output_filename': 'js/jquery-legacy.min.js',
    },
    'youckan-common': {
        'source_filenames': (
            'bower/bootstrap/dist/js/bootstrap.js',
            'bower/jquery.cookie/jquery.cookie.js',
            'bower/jquery.validation/jquery.validate.js',
            'bower/typeahead.js/dist/typeahead.js',
            'bower/swig/index.js',
            'bower/etalab-assets/js/etalab-site.js',
            # 'js/djangojs/django.js',
            'js/common.js',
        ),
        'output_filename': 'js/youckan.min.js'
    },
    'home': {
        'source_filenames': (
            'js/home.js',
        ),
        'output_filename': 'js/home.min.js',
    },

}
