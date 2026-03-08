def build_prompt(data):

    prompt = f"""
    Create a professional motorcycle promotional poster.

    Bike Model: {data.bike_model}
    Bike Color: {data.bike_color}
    Poster Background: {data.background}
    Platform: {data.platform}
    Language: {data.language}
    Dealer Name: {data.dealer_name}

    Style: Modern, high quality marketing poster suitable for social media.
    """

    return prompt