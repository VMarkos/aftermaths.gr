import re
import random

class LLM:
    def __init__(self, text, drop_punc = True, window = 1):
        if drop_punc:
            text = re.sub("[,\#\-\"\(\)·«»—\:…]", " ", text)
        words = re.split("\s+|^\w", text)
        self.word_type = self.get_limits(words)
        words = [re.sub("[\.\!\?\;]", "", word) for word in words if re.sub("[\.\!\?\;]", "", word)]
        self.raw_words, self.words, self.word_frequencies = self.get_words(words)
        self.word_distribution = self.get_wd()
        # self.word_type = self.get_limits()
        self.transition_probabilities = self.get_trans_prob(window)
        # self.transition_probabilities = self.get_tp()

    def get_limits(self, words):
        seen_delim = False
        DELIMS = [".", "!", "?", ";"]
        word_type = {re.sub("[\.\!\?\;]", "", word).lower() : 0 for word in words}
        for word in words:
            if re.sub("[\.\!\?\;]", "", word) == "":
                continue
            word = word.lower()
            # print(word, len(word))
            if seen_delim:
                word = re.sub("[\.\!\?\;]", "", word)
                if word_type[word] == 2:
                    word_type[word] == 3 # 3 means both
                else:
                    word_type[word] = 1 # 1 means start
                seen_delim = False
            # print(word, len(word))
            if word[-1] in DELIMS:
                word = re.sub("[\.\!\?\;]", "", word)
                if word_type[word] == 1:
                    word_type[word] = 3
                else:
                    word_type[word] = 2 # 2 means end
                seen_delim = True
            else:
                seen_delim = False
        # print("Ο" in [x for x, y in word_type.items() if y == 2])
        return word_type

    def export(self):
        json = {
            "words": self.words,
            "frequencies": self.word_frequencies,
            "distribution": self.word_distribution,
            "transition_probabilities": self.transition_probabilities,
        }
        return json

    def get_wd(self):
        wd = []
        cum_freq = 0
        for word, frequency in self.word_frequencies.items():
            cum_freq += frequency
            wd.append((cum_freq, word))
        return wd

    def get_words(self, words):
        raw_words = []
        original_words = []
        word_frequencies = {}
        step = 1 / len(words)
        for word in words:
            word = word.strip()
            if word != "":
                raw = word.lower()
                raw_words.append(raw)
                original_words.append(word)
                if raw not in word_frequencies.keys():
                    word_frequencies[raw] = step
                else:
                    word_frequencies[raw] += step
        return raw_words, original_words, word_frequencies

    def get_trans_prob(self, window):
        tp = {}
        for i in range(1, len(self.words) - window):
            previous = self.raw_words[max(0, i - window): i]
            if self.word_type[previous[-1]] == 2:
                continue
            current = self.raw_words[i]
            previous_hash = "|".join(previous)
            if previous_hash not in tp.keys():
                tp[previous_hash] = {}
            if current not in tp[previous_hash].keys():
                tp[previous_hash][current] = 1
            else:
                tp[previous_hash][current] += 1
        for p_hash, probs in tp.items():
            total = sum(list(probs.values()))
            for current in probs.keys():
                # print(probs, tp[p_hash].values(), tp[p_hash][current])
                tp[p_hash][current] /= total
        return tp

    def get_tp(self):
        tp = {}
        for i in range(len(self.words) - 1):
            current = self.raw_words[i]
            next = self.raw_words[i + 1]
            if current not in tp.keys():
                tp[current] = {}
            if next not in tp[current].keys():
                tp[current][next] = 1
            else:
                tp[current][next] += 1
        for word, probs in tp.items():
            for next in probs.keys():
                tp[word][next] /= sum(list(probs.values()))
        return tp
    
    def get_starting_word(self, rn):
        total = 0
        start_d = {}
        for word in self.raw_words:
            if self.word_type[word] not in [1, 3]:
                continue
            f = self.word_frequencies[word]
            total += f
            if word in start_d.keys():
                start_d[word] += f
            else:
                start_d[word] = f
        c_f = 0
        # print(count, len(self.raw_words), already_in, sum(list(start_d.values())), total)
        for word, f in start_d.items():
            if c_f >= rn:
                return word, False
            c_f += f / total
        # print(c_f, total)
        raise KeyError
    
    def random_pick(self, init = True, words = None, window = 1):
        rn = random.random()
        i = 0
        if init:
            return self.get_starting_word(rn)
        if not words:
            raise KeyError
        # print(words)
        # if window == 1:
        word = words[-1].lower()
        # else:
        #     word = "|".join([x.lower() for x in words[-window:len(words)]])
        if word not in self.transition_probabilities.keys():
            return None, True
        nexts = list(self.transition_probabilities[word].keys())
        cum_prop = 0
        next = None
        total = sum([self.get_tp(words, next) for next in nexts])
        while cum_prop < rn:
            next = nexts[i]
            # cum_prop += self.transition_probabilities[word][next]
            cum_prop += self.get_tp(words, next) / total
            i += 1
        next_index = self.raw_words.index(nexts[max(0, i - 1)])
        return self.words[next_index], self.word_type[self.raw_words[next_index]] in [2]

    def get_tp(self, words, next):
        last = words[-1].lower()
        if len(words) < 2:
            return self.transition_probabilities[last][next]
        second_last = words[-2].lower()
        try:
            return self.transition_probabilities[second_last][last] * self.transition_probabilities[last][next]
        except KeyError:
            return self.transition_probabilities[last][next]

    def generate_text(self, length = 10, window = 1):
        # one, two = self.random_pick()
        # text = [one, two]
        first_word = self.random_pick()[0]
        text = [first_word[0].upper() + first_word[1:]]
        # for i in range(length - 1):
        go = True
        i = 0
        while go:
            next_word, is_end = self.random_pick(init = False, words = text, window = window)
            # print(is_end, next_word)
            if not next_word:
                # print("not next word")
                text.append(self.random_pick()[0])
            elif is_end and i >= length:
                text.append(next_word + ".")
                go = False
            else:
                text.append(next_word)
            i += 1
        return " ".join(text)