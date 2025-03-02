# INF3203 - Distributed Systems
## Assignment 1: MapReduce and PageRank
### Authors

    Jens Christian Valen Leynse
    Email: jeley4465@uit.no

    Bjørn Helge Kværnmo
    Email: bkv005@uit.no

## How to Run the Program

Follow these steps to set up and run the MapReduce implementation of the PageRank algorithm:
## 1. Set Up the Environment

If you want to use a virtual environment (optional):
bash
Copy

``python3 -m venv .venv`` \
``source .venv/bin/activate`` \
``pip install -r requirements.txt``

## 2. Run the Sanity Check (Optional)

To ensure everything is set up correctly, run the sanity check script:
bash
Copy

``python3 run-sanity-check.py``

## 3. Run the Main Program

To execute the PageRank implementation, use the following command:
bash
Copy

``python3 testScript.py``

## 4. Modify Configuration (Optional)

You can adjust the number of mappers, reducers, and dataset size by editing the page-rank-config.json file.
## 5. View Results

    The results will be displayed in the terminal.

    Graphs and visualizations will be saved as image files (e.g., execution_time_all.png).

## Notes

    If you encounter issues with the virtual environment, you can run the project without it. Ensure Python 3 is installed and run the scripts directly.

    For any questions or issues, please contact the authors via their respective emails.