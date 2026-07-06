# Sentiment Analyzer (NLP with BERT)

Web application that analyzes the sentiment of a text and classifies it as
positive, negative or neutral, powered by a multilingual BERT model served
through the Hugging Face Inference API. The interface is intentionally
straightforward: enter a text, press a button, and get the predominant tone
along with its intensity.

## Use case

The primary scenario is **customer review analysis**. Any business that
receives feedback about its products or services needs to quickly understand
whether user perception is favorable or not, especially as the volume of
opinions grows and reading them one by one becomes impractical.

With this tool, a member of a customer support or product team can paste a
customer's comment and instantly know whether it expresses satisfaction,
dissatisfaction or a neutral stance, as well as the intensity with which the
model holds that classification. The page includes three sample reviews that
let you try the application's behavior with a single click, without having to
write your own text.

Although the example focuses on reviews, the same logic applies to other
contexts where measuring the tone of free-form text is useful, such as survey
responses, support messages or social media posts.

## Tools used

| Area | Tool |
|------|------|
| Language | Python 3 |
| Web framework | Flask (application factory pattern with blueprints) |
| AI model | `nlptown/bert-base-multilingual-uncased-sentiment` (BERT) via the Hugging Face Inference API |
| HTTP client | `requests` library |
| Interface | HTML5, CSS3 and JavaScript (with the `fetch` API) |
| Typography | Inter (titles) and IBM Plex Mono (body), via Google Fonts |
| Iconography | Inline SVG icons |
| Screenshots | Playwright (browser automation) |

## Project structure

```
practice_project/
├── app/                    # Flask application package
│   ├── __init__.py         # Application factory
│   ├── routes.py           # Routes / endpoints
│   ├── analyzer.py         # Sentiment service client
│   ├── static/
│   │   ├── css/styles.css
│   │   └── js/main.js
│   └── templates/
│       └── index.html
├── docs/screenshots/       # Interface screenshots
├── run.py                  # Local entry point
├── wsgi.py                 # WSGI entry point (Vercel / production)
├── vercel.json             # Vercel deployment configuration
├── requirements.txt
├── LICENSE
└── README.md
```

## Screenshots

### Positive sentiment

When the text conveys satisfaction, the result is shown in green with a smiling
face icon and the intensity computed by the model.

![Positive sentiment state](docs/screenshots/positive.png)

### Negative sentiment

For a text that expresses dissatisfaction, the result is presented in red with a
frowning face icon.

![Negative sentiment state](docs/screenshots/negative.png)

### Neutral sentiment

If the text does not lean toward either extreme, the result appears in a neutral
tone with an impassive face icon.

![Neutral sentiment state](docs/screenshots/neutral.png)

### Error state

When the input is empty or the service is unavailable, the application does not
crash: it shows a descriptive message in amber accompanied by a warning icon,
informing the user of what happened.

![Error state](docs/screenshots/error.png)

## Installation and usage

The app calls the Hugging Face Inference API, so it needs a free access token
set in the `HF_TOKEN` environment variable.

```bash
pip install -r requirements.txt

# Linux / macOS
export HF_TOKEN="hf_your_token_here"
# Windows (PowerShell)
$env:HF_TOKEN = "hf_your_token_here"

python run.py
```

Then open <http://localhost:5000> in your browser.

You can create a free token at
<https://huggingface.co/settings/tokens> (a token with the default "Read"
role is enough).

## Deploying on Vercel

The repository is ready to deploy on Vercel as a single Python Function:

- `wsgi.py` exposes the Flask `app` instance that Vercel looks for.
- `vercel.json` configures that function: it bundles the `app/` templates and
  static assets and raises the timeout to accommodate the model's cold start.

Steps:

1. Push this repository to your own GitHub account and import it in Vercel.
2. In **Project Settings → Environment Variables**, add `HF_TOKEN` with your
   Hugging Face token.
3. Deploy. Vercel installs `requirements.txt` automatically.

## License

[MIT](LICENSE) © 2026 Wesley Ruiz
