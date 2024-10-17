from setuptools import setup, find_packages


setup(
    name="karp_wa_automation",
    version=1,
    description="Whatsapp automation",
    author="Karp Infotech",
    author_email="sushil.pal@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'selenium>=4.0.0',  # Add Selenium as a dependency
    ]
)
