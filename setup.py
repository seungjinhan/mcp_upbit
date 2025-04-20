from setuptools import setup, find_packages

setup(
    name="mcp_upbit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # 필요한 외부 라이브러리 추가
    ],
    entry_points={
        'console_scripts': [
            'your-mcp-server=mcp_upbit.server:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Model Context Protocol server without API key",
    keywords="mcp, server",
    python_requires='>=3.7',
)