import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import plotly.express as px
import nltk
from wordcloud import WordCloud
from nltk import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter
from dash import dcc
import re

nltk.download("punkt_tab")


def get_ngram_freq(df, feature, n_list, sort_by_values=True):

    def generate_ngrams(text, n):
        tokens = word_tokenize(text)
        return list(ngrams(tokens, n))

    all_ngrams = []
    for n in n_list:
        for text in df[feature]:
            all_ngrams.extend(generate_ngrams(text, int(n)))

    ngram_freq = Counter(all_ngrams)

    word_frequencies = {" ".join(ngram): freq for ngram, freq in ngram_freq.items()}
    if sort_by_values:
        word_frequencies = {
            k: v
            for k, v in sorted(
                word_frequencies.items(), key=lambda item: item[1], reverse=True
            )
        }
    return word_frequencies


def truncate_cmap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap


def generate_dash_component(id, fig):
    return dcc.Graph(
        id=f"wordcloud_{id}",
        figure=fig,
        config={
            "displayModeBar": True,
            "autosizable": True,
            "responsive": True,
            "scrollZoom": True,
        },
        style={"height": "60vh", "width": "100%"},
    )


def generate_wordcloud_fig(wordcloud_image):
    fig = px.imshow(wordcloud_image)
    fig.update_layout(
        title={
            "text": "Job Title Frequency Word Cloud",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin={"t": 50, "b": 0, "l": 0, "r": 0},
        hovermode=False,
        paper_bgcolor="#F9F9FA",
        plot_bgcolor="#F9F9FA",
    )
    return fig


def generate_wordcloud_div(wordcloud_exclusions, input_df, id):
    """
    Function that will generate and save wordcloud.
    Text being analyzed already has general stopwords
    removed from earlier preprocessing. Will exclude
    search query only.
    Classname will be used in filename.
    """

    # instantiate wordcloud
    wordcloud = WordCloud(
        min_font_size=4,
        scale=2.5,
        background_color="#F9F9FA",
        collocations=True,
        regexp=r"[a-zA-z#&]+",
        min_word_length=4,
        colormap=truncate_cmap(plt.get_cmap("ocean"), 0, 0.7),
        random_state=0,
    )

    # generate image
    word_frequencies = get_ngram_freq(input_df, "job_title", np.arange(1, 4))
    for key in wordcloud_exclusions:
        word_frequencies.pop(key, None)
    wordcloud_image = wordcloud.generate_from_frequencies(word_frequencies)
    wordcloud_image = wordcloud_image.to_array()
    fig = generate_wordcloud_fig(wordcloud_image)
    return generate_dash_component(id, fig)


def adjusted_rgba(rgba, factor=0.7):
    """
    Lighten an RGBA color string by mixing it with white.

    Parameters:
    - rgba (str): A string representing the original color in the format 'rgba(r, g, b, a)'.
    - factor (float): The factor by which to lighten the color. Default is 0.3.
                      Should be between 0 and 1.

    Returns:
    - str: A lighter version of the original RGBA color as a string.
    """
    # Extract the rgba components from the input string
    match = re.match(r"rgba\((\d+), (\d+), (\d+), ([0-9.]+)\)", rgba)
    if not match:
        raise ValueError(f"Invalid RGBA string format: {rgba}")

    r, g, b, a = map(float, match.groups())

    # Ensure factor is between 0 and 1
    factor = min(1, max(0, factor))

    # Calculate lighter color by interpolating between the color and white (255, 255, 255)
    new_r = int(r + factor * (255 - r))
    new_g = int(g + factor * (255 - g))
    new_b = int(b + factor * (255 - b))

    # Return the lighter color as a string
    return f"rgba({new_r}, {new_g}, {new_b}, {a})"
