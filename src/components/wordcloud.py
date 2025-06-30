from utils.helper import generate_wordcloud_div


def create_wordcloud(wordcloud_exclusions, input_df, id):
    return generate_wordcloud_div(wordcloud_exclusions, input_df, id)
