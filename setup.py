import setuptools
import platform

if platform.system() == "Windows":
    extra_compile_args = ["/std:c++20"]
else:
    extra_compile_args = ["-std=c++20"]


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="chart",
    version="0.0.1",
    license="MIT",
    author="Arendelle",
    author_email="2381642961@qq.com",
    description="drow you ascii art on your terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoodenoughPhysicsLab/char_art.git",
    packages=setuptools.find_packages(),
    install_requires=["opencv-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    ext_modules=[
        setuptools.Extension(
            name="chart_cpp",
            language="c++",
            sources=["chart_cpp/impl.cpp"],
            extra_compile_args=extra_compile_args,
        )
    ]
)
