from flask import Flask, render_template_string, Response
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def load_dataframe():
    # Specify the path to your file
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 28\sq.us.txt"

    try:
        # Load the file into a Pandas DataFrame
        df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'])

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
                <h1 class="mt-5">Filtered DataFrame Preview</h1>
                {html_table}
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template)
    except Exception as e:
        return f"An error occurred while processing the file: {e}"

@app.route('/2016_monthly_average')
def monthly_average_open():
    # Specify the path to your file
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 28\sq.us.txt"

    try:
        # Load the file into a Pandas DataFrame
        df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'])

        # Filter the DataFrame for dates within the specified range
        start_date = "2016-01-01"
        end_date = "2016-12-31"
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Calculate the monthly average "Open" price
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_open_avg = df.groupby('Month')['Open'].mean()
        monthly_high_avg = df.groupby('Month')['High'].mean()
        monthly_low_avg = df.groupby('Month')['Close'].mean()

        # Plot the data
        plt.figure(figsize=(10, 6))
        monthly_open_avg.plot(color='black', linestyle='-', marker='o', label='Monthly Avg Open Price')
        monthly_high_avg.plot(color='green', linestyle='-', marker='o', label='Monthly Avg High Price')
        monthly_low_avg.plot(color='red', linestyle='-', marker='o', label='Monthly Avg Close Price')
        plt.title('Monthly Average Prices (2016)', fontsize=16)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Average Prices', fontsize=12)
        plt.grid(True)
        plt.legend()

        # Save the plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return Response(buf, mimetype='image/png')
    except Exception as e:
        return f"An error occurred while processing the file: {e}"

if __name__ == '__main__':
    app.run(debug=True)
