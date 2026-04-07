from setuptools import find_packages, setup

setup(
    name="wordtraductor",
    version="0.1.0",
    description="Translate Word documents from Google Drive via CLI.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "python-docx==0.8.11",
        "google-api-python-client==2.100.0",
        "google-auth-oauthlib==1.2.0",
        "argostranslate",
        "click==8.1.7",
        "tqdm==4.66.1",
        "python-dotenv==1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "wordtraductor=wordtraductor.cli.main:main",
        ]
    },
)
