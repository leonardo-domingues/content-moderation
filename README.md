# content-moderation

## About the solution

The solution was planned to be run as two separate processes. The first one is responsible for receiving blog posts via a POST call and registering them on the database. The second process periodically looks for unverified posts on the database and checks if they contain any foul words using the specified REST API. If there is an error while validating any of the post's paragraphs, that paragraph will be kept marked as unverified. The next time the validator is run for that post, only the unverified paragraphs will be checked.

## Setup
All requirements are included in the `requirements.txt` file.

I ended up using NLTK to separate the paragraphs into sentences so I had a more robust splitter. In retrospect, I should have just implemented a simple splitter that looks for period(`.`) characters. Because of that decision, there is an extra step needed to download the NLTK data after installing the requirements. These commands have to be run on the Python interpreter, as they will require user input:

```python
>>> import nltk
>>> nltk.download()
```
Then, press `d` for download and install the `punkt` package.

The scripts `run_api_and_moderator.sh` can be used to launch both the REST API controller and the ContentModerator process, although there is not much use to running them, seeing as the API to process sentences is not available. Running this script will launch the REST API, but the ContentModerator will continuously try to process every blog post found in the database.

The python scripts `src/launch_API.py` and `src/launch_ContentModerator.py` can be used directly to launch each part of the solution separately, but they require the `PYTHONPATH` environment variable to be set as the root directory of the repository.

The `run_tests.sh` can be used to run the unit tests.
