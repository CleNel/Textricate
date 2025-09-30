import os
import pdfplumber
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

PREVIEW_FOLDER = "previews"
os.makedirs(PREVIEW_FOLDER, exist_ok=True)


def preview_page_with_boxes(pdf_path, page_num=0, boxes=None):
    filename = os.path.basename(pdf_path)
    name, _ = os.path.splitext(filename)
    preview_path = os.path.join(PREVIEW_FOLDER, f"{name}_page{page_num+1}.png")

    # Return cached if exists and no new boxes
    if os.path.exists(preview_path) and not boxes:
        return preview_path

    with pdfplumber.open(pdf_path) as pdf:
        if page_num >= len(pdf.pages):
            raise ValueError(f"Page {page_num} not found in PDF")

        page = pdf.pages[page_num]

        fig, ax = plt.subplots(1, figsize=(10, 14))
        img = page.to_image(resolution=150).original
        ax.imshow(img, cmap="gray", extent=[0, page.width, 0, page.height])

        # Draw boxes if given
        if boxes:
            for bbox in boxes:
                x0, y0, x1, y1 = bbox
                ax.add_patch(Rectangle(
                    (x0, page.height - y1),
                    x1 - x0,
                    y1 - y0,
                    linewidth=2, edgecolor='green', facecolor='none'
                ))

        ax.axis("off")
        plt.savefig(preview_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

    return preview_path


def extract_text_from_boxes(pdf_path, page_num, boxes):
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        if page_num >= len(pdf.pages):
            raise ValueError(f"Page {page_num} not found in PDF")

        page = pdf.pages[page_num]
        for bbox in boxes:
            x0, y0, x1, y1 = bbox
            text = page.crop((x0, y0, x1, y1)).extract_text() or ""
            extracted_text.append(text.strip())
    return extracted_text

def extract_all_pages_with_boxes(pdf_path, bboxes_per_page):
    all_text = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, boxes in bboxes_per_page.items():
            page_num = int(page_num)  # ensure integer
            all_text[page_num] = extract_text_from_boxes(pdf_path, page_num, boxes)
    return all_text

