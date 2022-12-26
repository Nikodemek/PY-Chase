import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='chase',
    version='1.0.0',
    author='Nikodem Kirsz 236559',
    author_email='236550@edu.p.lodz.pl',
    description='Simulation of catching sheep by a wolf.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nikodemek/PY-Chase',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.10'
)
