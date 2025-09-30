# Textricate

A Flask application for previewing PDFs, drawing bounding boxes on them, and extracting text from selected regions.

---

## Features

* Upload PDF files
* Preview full pages without cropping
* Draw bounding boxes on PDF pages
* Extract text from selected bounding boxes

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/CleNel/Textricate.git
cd pdf-box-drawer
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

In the root directory of the project, create a file called `.env` with the following contents:

```
FLASK_SECRET_KEY=my-super-secret-key
UPLOAD_FOLDER=uploads
PREVIEW_FOLDER=previews
```

Replace `my-super-secret-key` with your own secure key.

### 5. Run the app

```bash
flask run
```

The app will be available at `http://127.0.0.1:5000/static/index.html`.

---

## Usage

1. Open the app in your browser.
2. Upload a PDF file using the upload form.
3. Use navigation buttons to move between pages.
4. Draw bounding boxes on the PDF preview.
5. Click **Extract Text** to get text from selected boxes.
6. Use **Clear Boxes** to remove drawn regions.

---

## Project Structure

```
pdf-box-drawer/
│
├── app.py              # Flask backend
├── requirements.txt    # Dependencies
├── .gitignore          # Ignored files
├── README.md           # Documentation
├── .env                # Environment variables
├── uploads/            # Uploaded PDFs (ignored by git)
├── previews/           # PDF previews (ignored by git)
├── static/
│   ├── style.css       # CSS styles
│   ├── index.html      # Frontend page
│   └── app.js          # Frontend JavaScript
```

---

## Security

* `.env` contains sensitive information (like `FLASK_SECRET_KEY`) and should **never** be committed to GitHub.
* `.gitignore` prevents sensitive files and large uploads from being tracked.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

* [Flask](https://flask.palletsprojects.com/)
* [pdfplumber](https://github.com/jsvine/pdfplumber)
* [Fabric.js](http://fabricjs.com/)
