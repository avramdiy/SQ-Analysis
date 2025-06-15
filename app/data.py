from flask import Flask, render_template_string, Response, request
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
        <div class="table-responsive">
            {html_table}
        </div>
        <h2 class="mt-5">Select a Month to Visualize Data</h2>
        <form action="/visualize_month" method="get">
            <div class="form-group">
                <label for="month">Choose a month:</label>
                <select name="month" id="month" class="form-control" required>
                    <option value="" disabled selected>Select a month</option>
                    <option value="1">January</option>
                    <option value="2">February</option>
                    <option value="3">March</option>
                    <option value="4">April</option>
                    <option value="5">May</option>
                    <option value="6">June</option>
                    <option value="7">July</option>
                    <option value="8">August</option>
                    <option value="9">September</option>
                    <option value="10">October</option>
                    <option value="11">November</option>
                    <option value="12">December</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary mt-3">Submit</button>
        </form>
    </div>
</body>
</html>
"""

        return render_template_string(html_template)
    except Exception as e:
        return f"An error occurred while processing the file: {e}"

@app.route('/visualize_month', methods=['GET'])
def visualize_month():
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 28\sq.us.txt"

    try:
        # Load the file into a Pandas DataFrame
        df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'])

        # Filter the DataFrame for dates within the specified range
        start_date = "2016-01-01"
        end_date = "2016-12-31"
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Check if a month is selected
        selected_month = request.args.get('month')

        if not selected_month:
            # Render a page with the dropdown to select a month
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Select a Month</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body>
                <div class="container">
                    <h1 class="mt-5">Select a Month to Visualize Data</h1>
                    <form action="/visualize_month" method="get">
                        <div class="form-group">
                            <label for="month">Choose a month:</label>
                            <select name="month" id="month" class="form-control" required>
                                <option value="" disabled selected>Select a month</option>
                                <option value="1">January</option>
                                <option value="2">February</option>
                                <option value="3">March</option>
                                <option value="4">April</option>
                                <option value="5">May</option>
                                <option value="6">June</option>
                                <option value="7">July</option>
                                <option value="8">August</option>
                                <option value="9">September</option>
                                <option value="10">October</option>
                                <option value="11">November</option>
                                <option value="12">December</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary mt-3">Submit</button>
                    </form>
                </div>
            </body>
            </html>
            """
            return render_template_string(html_template)

        # Convert the selected month to integer
        selected_month = int(selected_month)

        # Filter the data for the selected month
        df = df[df['Date'].dt.month == selected_month]

        if df.empty:
            return f"No data available for the selected month ({selected_month})."

        # Plot the "Open" price for the selected month
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Open'], color='black', marker='o', label='Open Price')
        plt.plot(df['Date'], df['High'], color='green', marker='o', label='Open Price')
        plt.plot(df['Date'], df['Low'], color='red', marker='o', label='Open Price')
        plt.title(f"Prices for Month {selected_month} (2016)", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Prices", fontsize=12)
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
