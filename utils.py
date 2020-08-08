import re

def pre_processing(text):
    """
    :type text: str
    """
    text = re.sub("-\n", "", text)
    text = re.sub("\n", " ", text)
    return text