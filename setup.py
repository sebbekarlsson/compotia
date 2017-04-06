from distutils.core import setup
import setuptools
import subprocess


setup(
    name='compotia',
    version='1.1',
    install_requires=[
        'watchdog',
        'requests',
        'Jinja2',
        'pytest',
        'libsass'
    ],
    packages=[
        'compotia',
    ],
    entry_points={
        "console_scripts": [
            "compotia = compotia.program:run"
        ]
    }
)


subprocess.call(['mkdir', '/tmp/compotia'])
subprocess.Popen('cp -r ./compotia/internal/templates/ /tmp/compotia/.', shell=True)
subprocess.Popen('cp -r ./compotia/internal/components/ /tmp/compotia/.', shell=True)
