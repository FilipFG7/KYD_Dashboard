# KYD_Dashboard

## Main file- Dashapp.py

Creates and runs an app in dash using python language. Builds a basic layout of the page that consist of a responsive header, dropdown to choose pages and the rest of the layout is determined by the page layout.

## Main page- Algorithmpage.py

Creates a layout with an upload window, where the users selects a file with the customers data (Customer.xlsx). This file is then saved using callback and functions. Furthermore it displays an output of text to confirm the file has been saved. Once the file is saved, the user presses the submit button which acts as an input for a callback that starts a machine learning algorithm. This algorithm predicts the customers' income based on the data provided by user plus the ifood_df.csv file. After the prediction is done, it is presented as an data table on the dashboard.

## Second page- DataTable.py

Creates a layout with a markdown, range slider and mainly the data table. The range slider adjusts the range of values of the income.
