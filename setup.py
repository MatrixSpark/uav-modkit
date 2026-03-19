from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'uav_modkit'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='UAV Development Team',
    author_email='dev@example.com',
    description='Unified UAV modular kit with sensors (IMU, LiDAR, Power) and management modules',
    license='Apache-2.0',
    url='https://github.com/yourusername/uav-modkit',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [],
    },
)
