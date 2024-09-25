import re

def extract_image_info(markdown_file):
    # Regex pattern to find image markdown
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'

    with open(markdown_file, 'r', encoding='utf-8') as file:
        content = file.read()

    matches = re.findall(pattern, content)

    for alt_text, img_src in matches:
        # Print the Jekyll include format
        print(f'{{% include lazyimg.html img_src="{img_src}" img_alt="{alt_text}" %}}')

if __name__ == "__main__":
    # Replace 'your_file.md' with the path to your Markdown file
    markdown_file = '2024-09-21-malware-analysis-pxrecvoweiwoei.md'
    extract_image_info(markdown_file)
