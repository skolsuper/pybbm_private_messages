import django
import sys
import os
from optparse import OptionParser
from django.test.runner import DiscoverRunner as Runner

project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
sys.path.insert(0, project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pybbm_private_messages.settings')


def runtests(*test_args, **kwargs):
    django.setup()

    if not test_args:
        test_args = ['private_messages']

    test_runner = Runner(verbosity=kwargs.get('verbosity', 1), interactive=kwargs.get('interactive', False),
                         failfast=kwargs.get('failfast'))
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true', default=False, dest='failfast')

    (options, args) = parser.parse_args()

    runtests(failfast=options.failfast, *args)
