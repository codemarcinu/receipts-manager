from setuptools import setup, find_packages

setup(
    name="receipts-manager",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-wtf',
        'python-dotenv',
        'Pillow',
        'google-cloud-vision'
    ],
)