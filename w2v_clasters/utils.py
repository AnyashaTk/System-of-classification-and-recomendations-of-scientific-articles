from constants import *

TOKEN_RE = re.compile(r'[\w\d]+')


def get_texts(files_names):
    texts_all = [pd.read_csv(path1 + file)['0'].dropna() for file in files_names]
    all_tokenized = [(tokenize_corpus(text)) for text in texts_all]
    texts_like_one = []
    for token_text in all_tokenized:
        for str in token_text:
            texts_like_one.append(str)
    return all_tokenized, texts_like_one

def get_many_columns(files_names):
    files = [pd.read_csv(path + file).dropna()for file in files_names]
    data = []
    texts = pd.DataFrame()
    for file in files:
        for num in range(file.shape[0]):
            '''txt = 0
            for word in tokenize_corpus(file['text'])[num]:
                txt += model_w2v.wv[word]'''
            data.append([float(file['space_num'][num]), float(file['symbolic_percent'][num]),
                         float(file['space_percent'][num]), float(file['num_world'][num]),
                         float(file['num_columns'][num]), float(file['front_spaces_perc'][num]),
                         float(file['back_spaces'][num])])
        texts = pd.concat([texts, file['text']], ignore_index=True)
    return data, texts

def tokenize_text_simple_regex(txt, min_token_size=4):
    txt = txt.lower()
    all_tokens = TOKEN_RE.findall(txt)
    return [token for token in all_tokens if len(token) >= min_token_size]


def character_tokenize(txt):
    return list(txt)


def tokenize_corpus(texts, tokenizer=tokenize_text_simple_regex, **tokenizer_kwargs):
    return [tokenizer(text, **tokenizer_kwargs) for text in texts]


def build_vocabulary(tokenized_texts, max_size=1000000, max_doc_freq=0.8, min_count=5, pad_word=None):
    word_counts = collections.defaultdict(int)
    doc_n = 0

    # посчитать количество документов, в которых употребляется каждое слово
    # а также общее количество документов
    for txt in tokenized_texts:
        doc_n += 1
        unique_text_tokens = set(txt)
        for token in unique_text_tokens:
            word_counts[token] += 1

    # убрать слишком редкие и слишком частые слова
    word_counts = {word: cnt for word, cnt in word_counts.items()
                   if cnt >= min_count and cnt / doc_n <= max_doc_freq}

    # отсортировать слова по убыванию частоты
    sorted_word_counts = sorted(word_counts.items(),
                                reverse=True,
                                key=lambda pair: pair[1])

    # добавим несуществующее слово с индексом 0 для удобства пакетной обработки
    if pad_word is not None:
        sorted_word_counts = [(pad_word, 0)] + sorted_word_counts

    # если у нас по прежнему слишком много слов, оставить только max_size самых частотных
    if len(word_counts) > max_size:
        sorted_word_counts = sorted_word_counts[:max_size]

    # нумеруем слова
    word2id = {word: i for i, (word, _) in enumerate(sorted_word_counts)}

    # нормируем частоты слов
    word2freq = np.array([cnt / doc_n for _, cnt in sorted_word_counts], dtype='float32')

    return word2id, word2freq


def vectorize(line, w2v_indices, w2v_vectors):
    words = []
    for word in line:  # line - iterable, for example list of tokens
        try:
            w2v_idx = w2v_indices[word]
        except KeyError:  # if you does not have a vector for this word in your w2v model, continue
            continue
        words.append(w2v_vectors[w2v_idx])
        if words:
            words = np.asarray(words)
            min_vec = words.min(axis=0)
            max_vec = words.max(axis=0)
            return np.concatenate((min_vec, max_vec))
        if not words:
            return None
