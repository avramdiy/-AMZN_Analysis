from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Flask API to Load Path Data</h1><p>Visit /load to see the dataframe.</p>"

@app.route('/load', methods=['GET'])
def load_file():
    file_path = "C:\\Users\\avram\\OneDrive\\Desktop\\TRG Week 24\\amzn.us.txt"

    if not os.path.exists(file_path):
        return {"error": "File does not exist"}, 404

    try:
        # Adjust delimiter if needed, e.g., delimiter='\t'
        df = pd.read_csv(file_path)

        html_table = df.to_html(classes='table table-striped', index=False)

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>DataFrame Viewer</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container mt-4">
                <h2>$AMZN DATA</h2>
                {html_table}
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template)

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
