import os
import pdfplumber
from flask import Flask, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

UPLOAD_FOLDER = "uploads"
PREVIEW_FOLDER = "previews"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREVIEW_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]
        safe_name = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, safe_name)
        file.save(filepath)

        session["pdf_path"] = filepath
        session["filename"] = safe_name

    pdf_path = session.get("pdf_path")
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"error": "No file uploaded"}), 400

    page = int(request.args.get("page", 0))

    with pdfplumber.open(pdf_path) as pdf:
        if page >= len(pdf.pages):
            return jsonify({"error": "Page out of range"}), 400

        page_obj = pdf.pages[page]
        page_width, page_height = page_obj.width, page_obj.height

        # Save full-page preview
        preview_filename = f"{session['filename']}_page{page}.png"
        preview_path = os.path.join(PREVIEW_FOLDER, preview_filename)
        page_obj.to_image().save(preview_path)

        return jsonify({
            "preview_url": f"/previews/{preview_filename}",
            "page_width": page_width,
            "page_height": page_height,
            "total_pages": len(pdf.pages)
        })


@app.route("/previews/<path:filename>")
def serve_preview(filename):
    return send_file(os.path.join(PREVIEW_FOLDER, filename), mimetype="image/png")


@app.route("/extract", methods=["POST"])
def extract_boxes():
    data = request.json
    filename = data.get("filename")
    bboxes_per_page = data.get("bboxes_per_page")

    if not filename or not bboxes_per_page:
        return {"error": "Missing filename or bboxes_per_page"}, 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return {"error": "File not found"}, 404

    texts = {}

    with pdfplumber.open(filepath) as pdf:
        for page_num, boxes in bboxes_per_page.items():
            page_num = int(page_num)
            if page_num >= len(pdf.pages):
                continue

            page = pdf.pages[page_num]
            page_width, page_height = page.width, page.height

            texts[page_num] = []

            for box in boxes:
                x0, y0, x1, y1 = box

                # Clamp to page bounds
                x0 = max(0, min(x0, page_width))
                x1 = max(0, min(x1, page_width))
                y0 = max(0, min(y0, page_height))
                y1 = max(0, min(y1, page_height))

                cropped = page.crop((x0, y0, x1, y1))
                extracted_text = cropped.extract_text() or ""
                texts[page_num].append(extracted_text.strip())

    return jsonify({"texts": texts})


if __name__ == "__main__":
    app.run(debug=True)
