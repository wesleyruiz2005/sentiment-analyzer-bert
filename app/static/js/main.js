const analyzeBtn = document.getElementById("analyzeBtn");
const textInput = document.getElementById("textToAnalyze");
const resultBox = document.getElementById("result");

const SVG_ATTRS =
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"';

const ICONS = {
    positive:
        `<svg ${SVG_ATTRS}><circle cx="12" cy="12" r="10"/>` +
        `<path d="M8 14s1.5 2 4 2 4-2 4-2"/>` +
        `<line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>`,
    negative:
        `<svg ${SVG_ATTRS}><circle cx="12" cy="12" r="10"/>` +
        `<path d="M16 16s-1.5-2-4-2-4 2-4 2"/>` +
        `<line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>`,
    neutral:
        `<svg ${SVG_ATTRS}><circle cx="12" cy="12" r="10"/>` +
        `<line x1="8" y1="15" x2="16" y2="15"/>` +
        `<line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>`,
    error:
        `<svg ${SVG_ATTRS}>` +
        `<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>` +
        `<line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
};

const LABELS = {
    positive: { text: "Positive sentiment", css: "positive" },
    negative: { text: "Negative sentiment", css: "negative" },
    neutral: { text: "Neutral sentiment", css: "neutral" },
};

// Fill the text area when a sample review is clicked.
document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
        textInput.value = chip.dataset.text;
        textInput.focus();
    });
});

analyzeBtn.addEventListener("click", runSentimentAnalysis);

function showResult(cssClass, iconKey, html) {
    resultBox.className = `result ${cssClass}`;
    resultBox.innerHTML = `${ICONS[iconKey]}<div>${html}</div>`;
}

async function runSentimentAnalysis() {
    const text = textInput.value.trim();

    if (!text) {
        showResult("error", "error", "Enter some text to analyze.");
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing…";

    try {
        const response = await fetch(
            `sentimentAnalyzer?textToAnalyze=${encodeURIComponent(text)}`
        );
        const data = await response.json();

        if (!data.ok) {
            showResult("error", "error", data.message);
            return;
        }

        const info = LABELS[data.label] || LABELS.neutral;
        const intensity = (Math.abs(data.score) * 100).toFixed(1);
        showResult(
            info.css,
            data.label,
            `<strong>${info.text}</strong>
             <span class="result-score">Intensity: ${intensity}%</span>`
        );
    } catch (error) {
        showResult("error", "error", "Could not connect to the server. Please try again.");
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze sentiment";
    }
}
