from setuptools import setup


setup(
    name='cldfbench_concepticon',
    py_modules=['cldfbench_concepticon'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'concepticon=cldfbench_concepticon:Dataset',
        ],
        'cldfbench.commands': [
            'concepticon=concepticoncommands',
        ]
    },
    install_requires=[
        'csvw>=3.1.2',
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
