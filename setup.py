from setuptools import setup, find_packages
from setuptools.command.install import install

import os
import configparser
import traceback
from pandoctools.shortcut import ShortCutter
from pandoctools.cli import pandoctools_user
import versioneer
import io
import sys

DEFAULTS_INI = {'profile': 'Default',
                'out': '*.*.md',
                'root_env': '',
                'win_bash': r'%PROGRAMFILES%\Git\bin\bash.exe'}


class PostInstallCommand(install):
    """
    Post-installation for installation mode.
    """
    def run(self):
        error_log = io.StringIO()
        sc = ShortCutter(raise_errors=False, error_log=error_log)

        # Set pandoctools_core:
        if os.name == 'nt':
            pandoctools_core = os.path.join(sc.site_packages, 'pandoctools', 'bat')
            _pandoctools_core = os.path.join(sc.site_packages, 'pandoctools', 'sh')
            bash_append = ' (Bash)'
        else:
            pandoctools_core = os.path.join(sc.site_packages, 'pandoctools', 'sh')
            _pandoctools_core = pandoctools_core
            bash_append = ''

        # Create shortcuts:
        sc.create_desktop_shortcut('pandoctools', entry_point=True)
        ret = sc.create_menu_shortcut('pandoctools', entry_point=True)
        pandoctools_bin = ret[1]

        sc.makedirs(pandoctools_user, pandoctools_core, _pandoctools_core)
        sc.create_desktop_shortcut(pandoctools_user, 'Pandoctools User Data')
        sc.create_shortcut(pandoctools_core, pandoctools_user, 'Pandoctools Core Data')
        sc.create_shortcut(_pandoctools_core, pandoctools_user, 'Pandoctools Core Data' + bash_append)

        # Write INI:
        config_file = os.path.join(pandoctools_user, 'Defaults.ini')
        config = configparser.ConfigParser(interpolation=None)
        default_sect = DEFAULTS_INI.copy()
        if os.path.exists(config_file):
            config.read(config_file)
            try:
                d = config.items('Default')
                default_sect.update(dict(d))
            except configparser.NoSectionError:
                pass
        default_sect['pandoctools'] = pandoctools_bin
        if os.path.exists(os.path.expandvars(default_sect['win_bash'])):
            pandoctools_core = _pandoctools_core

        config['Default'] = default_sect
        with io.StringIO() as file:
            config.write(file)
            config_str = file.getvalue()
        try:
            with open(config_file, 'w') as file:
                config.write(file)
        except:
            print('WARNING: Failed to create ini file.\n\n' + ''.join(traceback.format_exc()), file=error_log)
            print('File:\n{}\n\n{}'.format(config_file, config_str), file=error_log)

        # Dump error log:
        print(error_log.getvalue(), file=open(os.path.join(os.path.expanduser('~'), 'pandoctools_install_error_log.txt'),
                                              'w', encoding="utf-8"))
        error_log.close()

        install.run(self)


setup(
    name='pandoctools-ready',
    version=0.1.0,
    cmdclass={'install': PostInstallCommand},

    description='Shortcuts and user data creation for pandoctools: https://github.com/kiwi0fruit/pandoctools',
    url='https://github.com/kiwi0fruit/pandoctools-ready',

    author='Peter Zagubisalo',
    author_email='peter.zagubisalo@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=['pandoctools'],
)
