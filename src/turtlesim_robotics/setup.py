from setuptools import setup

package_name = 'turtlesim_robotics'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='luqman',
    maintainer_email='noshluk2@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test_node = turtlesim_robotics.test:main',
            'w2_drive_robot = turtlesim_robotics.1_driving_node:main',
            'w3_go_to_goal = turtlesim_robotics.w3_a_go_to_goal:main',
            'w3_proportional_go_to_goal = turtlesim_robotics.w3_b_propertional_controller_goToGoal:main',
            'w4_kinematics_model_circular_error = turtlesim_robotics.w4_kinematics_circular_rotation:main',

        ],
    },
)
