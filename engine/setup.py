import setuptools

setuptools.setup(
    name="ml_model",
    version="0.0.1",
    author="hadji gagny",
    author_mail="hadjigagny93@gmail.com",
    description="NLP model for predict gold stock",
    url="https://github.com/hadjigagny93/gold-stocks-prediction",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

