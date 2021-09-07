import pandas as pd

texts = pd.read_csv("../texts.csv")
words_dict = {}
for text in texts["0"]:
    while "\n" in text:
        text = text.replace("\n", " ")
    while "\t" in text:
        text = text.replace("\t", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    words = text.strip().split(" ")
    for word in words:
        try:
            words_dict[word.lower()] += 1
        except KeyError:
            words_dict[word.lower()] = 1
text_dict = pd.DataFrame(columns=["word", "frec"])
text_dict["word"] = words_dict.keys()
text_dict["frec"] = words_dict.values()
text_dict.to_csv("text_dict.csv", index=False)
