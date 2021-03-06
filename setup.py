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
        from pandoctools.shared_vars import pandoctools_user, pandoctools_core
        from pyppdf.patch_pyppeteer import patch_pyppeteer
        from pyppeteer.command import install as install_chromium

        DEFAULTS_INI = {'profile': 'Default',
                        'out': '*.*.md',
                        'root_env': '',
                        'win_bash': r'%PROGRAMFILES%\Git\bin\bash.exe'}

        error_log = io.StringIO()
        sc = ShortCutter(raise_errors=False, error_log=error_log, activate=False)

        # Create shortcuts:
        sc.create_desktop_shortcut('pandoctools')
        pandoctools_bin = sc.create_menu_shortcut('pandoctools')[1]

        sc.makedirs(pandoctools_user)
        sc.create_desktop_shortcut(pandoctools_user, 'Pandoctools User Data')
        sc.create_shortcut(pandoctools_core, pandoctools_user, 'Pandoctools Core Data')

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

        config['Default'] = default_sect
        with io.StringIO() as file:
            config.write(file)
            config_str = file.getvalue()
        try:
            with open(config_file, 'w') as file:
                config.write(file)
        except:
            print(f'{traceback.format_exc()}\n'+
                  'WARNING: Failed to create ini file:\n'+
                  f'{config_file}\n\n{config_str}',
                  file=error_log)

        # Dump error log:
        error_log = error_log.getvalue().strip()
        if error_log:
            print(error_log, file=open(p.join(sc.desktop_folder, 'Error Log Pandoctools Install.txt'),
                                       'w', encoding="utf-8"))

        # Install chromium for pyppeteer:
        install_chromium()

        # ---------------
        install.run(self)


setup(
    name='pandoctools-ready',
    version='1.4.2',
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
        'Programming Language :: Python :: 3.6',
    ],

    install_requires=['shortcutter>=0.1.15', 'pandoctools'],
)
