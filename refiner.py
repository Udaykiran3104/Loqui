import re, yaml

class TextRefiner:
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)["refiner"]

        self.fillers = cfg.get("filler_words", [])
        self.fix_caps = cfg.get("fix_caps", True)
        self.fix_punct = cfg.get("fix_punctuation", True)

        # Build one regex pattern for all fillers (word boundaries)
        if self.fillers:
            escaped = [re.escape(f) for f in self.fillers]
            pattern = r'\b(?:' + '|'.join(escaped) + r')\b'
            self.filler_re = re.compile(pattern, re.IGNORECASE)
        else:
            self.filler_re = None

    def refine(self, text: str) -> str:
        # 1. Strip filler words
        if self.filler_re:
            text = self.filler_re.sub('', text)

        # 2. Collapse multiple spaces
        text = re.sub(r'\s{2,}', ' ', text).strip()

        # 3. Remove orphaned commas from filler removal (", ,")
        text = re.sub(r',\s*,', ',', text)
        text = re.sub(r'\s*,\s*\.', '.', text)

        # 4. Capitalize first letter
        if self.fix_caps and text:
            text = text[0].upper() + text[1:]

        # 5. Add period if no sentence-ending punctuation
        if self.fix_punct and text and text[-1] not in '.?!':
            text += '.'

        return text
