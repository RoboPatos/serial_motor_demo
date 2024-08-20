from setuptools import setup

package_name = 'serial_motor_demo'

setup(
    name=SciCoBot_2.0,
    version='2.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Natanael',
    maintainer_email='amilnatanael@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gui = serial_motor_demo.gui:main',
            'driver = serial_motor_demo.driver:main'
            'find_ports = serial_motor_demo.find_ports:main'
            'serial_teste = serial_motor_demo.serial_teste:main'
        ],
    },
)
