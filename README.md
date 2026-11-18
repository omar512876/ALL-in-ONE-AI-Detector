# ALL in ONE AI-detector

**CS50x 2026 Final Project** by Omar Mouaddeb ([omar512876](https://github.com/omar512876))

#### YouTube Video : [https://www.youtube.com/watch?v=ia3u_ijombs]

## Description

This is a small web app I built with Python and Flask. You paste a piece of text, and it tells you how likely it is that the text was written by an AI. It does this with two different detectors and shows you a separate score from each one, for example "72% likely AI". The score is green when it's low, orange in the middle and red when it's high.

## The two detectors

**Perplexity (GPT-2).** Perplexity is basically a measure of how surprised a language model is by a text. Text written by an AI is usually very predictable for a language model, so its perplexity is low. Human writing is messier and less predictable, so the perplexity is higher.
In my code I give the text to GPT-2, get the average loss, and turn it into perplexity with `exp(loss)`. Then I convert it to a score from 0 to 100: a perplexity of 15 or lower gives 100, 80 or higher gives 0, and anything in between is scaled in a straight line.
 I chose those two numbers by hand, so this score is more of a rough indicator than something precise.

**DistilBERT classifier.** The second detector is a DistilBERT model that was already trained to tell AI text from human text (on Hugging Face). The probability of the "AI" class times 100 is the score.

## Files

**app.py** has the Flask routes. `/` is the home page. `/analyze` shows the form with GET, and with POST it checks the input, runs every detector and shows the results.
The detectors are created once when the app starts and put in a list, so adding a third detector would only mean adding it to that list.

**helpers.py** has the `apology()` function that shows an error page with a message and a status code. I took the idea from the Finance problem set.

**detectors/base.py** has a `Detector` base class, so every detector gives back its result in the same format (name, source, score, error). It has three methods:
- `analyze()` is empty on purpose. Each detector has to replace it, and if one doesn't, it raises `NotImplementedError` so I notice right away.
- `result()` builds the result dictionary.
- `safe_analyze()` runs `analyze()` inside a try/except. If one detector fails, the page still works and just says that detector is unavailable, so the user still gets the other score.

I did it this way because the two detectors are very different inside, but the results page shouldn't have to care about that.

**detectors/perplexity.py** is the GPT-2 detector. It cuts the text at 512 tokens and refuses anything under 20 tokens, because a score from a few words wouldn't mean anything.

**detectors/bert_classifier.py** is the DistilBERT detector. It downloads the model's config file to get the max length, the temperature and the label mapping, so I didn't have to hard-code those values. It also uses the 20 token minimum.

**templates/** `layout.html` has the header and footer and the other pages extend it. `results.html` loops over the results, so a new detector shows up on its own  . `apology.html` has `role="alert"` so a screen reader reads the error out immediately.

**static/styles.css** is a small stylesheet I wrote with a little help of AI(claude). It uses CSS variables for the colors, works on small screens, and keeps a visible outline on focused elements for keyboard users.

## How to run it

1. create and activate a virtual environment (Optional) .
2. Install the requirements: `pip install -r requirements.txt`
3. From the project folder, run `flask run` and open the link

The first time you start it, it downloads GPT-2 and DistilBERT from Hugging Face. That takes a few minutes and a few hundred MB, so you need internet for the first run. After that it uses the cached files. It also takes a few seconds to start because both models are loaded into memory.

## Limitations

AI detection is not reliable, and I don't want to pretend this project fixes that.

- Long texts are cut, so only the first part is analyzed.
- Low perplexity doesn't prove a text is AI. Simple or formal writing can have low perplexity too, and so can writing by people who are not native English speakers.
- The classifier can be wrong, and how well it works depends on the style, length and topic of the text and on the data it was trained on.
## Use of AI tools

I got help from Claude (Anthropic) with undrestanding the structure of `perplexity.py` and `bert_classifier.py`, and `styles.css` as I wrote in the comments in  those files. I rewrote and tested the code myself.

## Technologies

Python, Flask, PyTorch, Hugging Face Transformers, HTML, CSS and Jinja.
