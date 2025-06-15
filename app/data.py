from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def load_dataframe():
    # Specify the path to your file
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 28\sq.us.txt"

    try:
        # Load the file into a Pandas DataFrame
        df = pd.read_csv(file_path, sep=",", engine="python")  # Adjust `sep` if not comma-delimited

        # Filter the DataFrame for dates within the specified range
        start_date = "2016-01-01"
        end_date = "2016-12-31"
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Drop the "OpenInt" column if it exists
        if 'OpenInt' in df.columns:
            df = df.drop(columns=['OpenInt'])

        # Convert the DataFrame to an HTML table
        html_table = df.to_html(classes='table table-striped', index=False)

        # Render the HTML table in a simple template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>DataFrame Viewer</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">DataFrame Preview</h1>
                {html_table}
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template)
    except Exception as e:
        return f"An error occurred while loading the file: {e}"

if __name__ == '__main__':
    app.run(debug=True)
