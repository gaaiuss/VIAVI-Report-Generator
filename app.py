from pathlib import Path

from flask import Flask, jsonify, request

from src.converter import mergeJsonFiles, saveToExcel, writeCsv  # type: ignore

app = Flask(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_files():
    uploaded_files = request.files.getlist("files")
    if not uploaded_files:
        return jsonify({"error": "No files received"}), 400

    saved_paths = []
    for file in uploaded_files:
        file_path = UPLOAD_DIR / file.filename  # type: ignore
        file.save(file_path)
        saved_paths.append(str(file_path))

    # Call your function with the uploaded files
    resource = mergeJsonFiles(saved_paths)

    # If you want, you can also write to CSV/Excel here
    writeCsv(resource)
    excel_path = saveToExcel("output.xlsx")

    return jsonify({
        "merged_count": len(resource),
        "saved_files": saved_paths,
        "excel_path": excel_path
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
