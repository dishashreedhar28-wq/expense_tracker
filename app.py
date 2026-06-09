from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
from collections import defaultdict
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

CSV_FILE = 'expenses.csv'

try:
    open(CSV_FILE, 'x').write('Date,Title,Category,Amount\n')
except:
    pass


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        amount = request.form['amount']

        date = datetime.now().strftime('%Y-%m-%d')

        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, title, category, amount])

        return redirect('/')

    expenses = []
    total = 0
    prediction = None
    category_totals = defaultdict(float)

    selected_month = request.args.get('month', '')

    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            month = row['Date'][:7]

            if selected_month == '' or month == selected_month:
                expenses.append(row)
                total += float(row['Amount'])
                category_totals[row['Category']] += float(row['Amount'])

    if len(expenses) >= 2:
        X = np.array(range(len(expenses))).reshape(-1, 1)
        y = np.array([float(exp['Amount']) for exp in expenses])

        model = LinearRegression()
        model.fit(X, y)

        next_expense = np.array([[len(expenses)]])
        prediction = round(model.predict(next_expense)[0], 2)

    return render_template(
        'index.html',
        expenses=expenses,
        total=total,
        category_totals=dict(category_totals),
        selected_month=selected_month,
        prediction=prediction
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

   





