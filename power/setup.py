from setuptools import setup, find_packages

package_name = 'power_mgr'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='UAV Development Team',
    author_email='dev@example.com',
    description='Power management and battery monitoring for UAV systems',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [],
    },
)
