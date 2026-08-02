import re
from pathlib import Path


def convert_markdown(input_file: str, folder: str):
    input_path = Path(input_file)

    output_path = input_path.with_name(f"{input_path.stem}__{input_path.suffix}")

    pattern = re.compile(r"!\[\[([^\]]+)\]\]")

    figure = 1

    def replace(match):
        nonlocal figure

        filename = match.group(1)
        stem = Path(filename).stem

        title = stem.replace("-", " ")

        replacement = (
            f"{{% include lazyimg.html "
            f'img_src="../assets/img/analysis/{folder}/lowly/{filename}" '
            f'img_datasrc="../assets/img/analysis/{folder}/{filename}" '
            f'img_caption="Figure {figure}: {title}" '
            f'img_alt="{title}" '
            f"%}}"
        )

        figure += 1
        return replacement

    text = input_path.read_text(encoding="utf-8")
    converted = pattern.sub(replace, text)

    output_path.write_text(converted, encoding="utf-8")

    print(f"Written: {output_path}")


if __name__ == "__main__":
    INPUT_FILE = "README.md"
    FOLDER_NAME = "easy"

    convert_markdown(INPUT_FILE, FOLDER_NAME)
