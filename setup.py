from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    """
    Post-installation for installation mode.
    """
    def run(self):
        import os
        from os import path as p
        import configparser
        import traceback
        import io
        import sys
        import inspect
        from shortcutter import ShortCutter
        import pandoctools
        from pandoctools.cli import pandoctools_user

        DEFAULTS_INI = {'profile': 'Default',
                        'out': '*.*.md',
                        'root_env': '',
                        'win_bash': r'%PROGRAMFILES%\Git\bin\bash.exe'}

        error_log = io.StringIO()
        sc = ShortCutter(raise_errors=False, error_log=error_log, activate=False)

        # Set pandoctools_core:
        pandoctools_dir = p.dirname(inspect.getfile(pandoctools))
        if os.name == 'nt':
            pandoctools_core = p.join(pandoctools_dir, 'bat')
            pandoctools_core2 = p.join(pandoctools_dir, 'sh')
            bash_append = ' (Bash)'
        else:
            pandoctools_core = p.join(pandoctools_dir, 'sh')
            pandoctools_core2 = pandoctools_core
            bash_append = ''

        # Create shortcuts:
        sc.create_desktop_shortcut('pandoctools')
        ret = sc.create_menu_shortcut('pandoctools')
        pandoctools_bin = ret[1]

        sc.makedirs(pandoctools_user)
        sc.create_desktop_shortcut(pandoctools_user, 'Pandoctools User Data')
        sc.create_shortcut(pandoctools_core, pandoctools_user, 'Pandoctools Core Data')
        sc.create_shortcut(pandoctools_core2, pandoctools_user, 'Pandoctools Core Data' + bash_append)

        # Write INI:
        config_file = p.join(pandoctools_user, 'Defaults.ini')
        config = configparser.ConfigParser(interpolation=None)
        default_sect = DEFAULTS_INI.copy()
        if p.exists(config_file):
            config.read(config_file)
            try:
                d = config.items('Default')
                default_sect.update(dict(d))
            except configparser.NoSectionError:
                pass
        default_sect['pandoctools'] = pandoctools_bin
        if p.exists(p.expandvars(default_sect['win_bash'])):
            pandoctools_core = pandoctools_core2

        config['Default'] = default_sect
        with io.StringIO() as file:
            config.write(file)
            config_str = file.getvalue()
        try:
            with open(config_file, 'w') as file:
                config.write(file)
        except:
            print('WARNING: Failed to create ini file.\n\n' + ''.join(traceback.format_exc()),
                  file=error_log)
            print('File:\n{}\n\n{}'.format(config_file, config_str), file=error_log)

        # Dump error log:
        print(error_log.getvalue(),
              file=open(p.join(p.expanduser('~'), 'pandoctools_install_error_log.txt'),
                        'w', encoding="utf-8"))
        error_log.close()

        # ---------------
        install.run(self)


setup(
    name='pandoctools-ready',
    version='0.1.0',
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

    install_requires=['shortcutter', 'pandoctools'],
)
