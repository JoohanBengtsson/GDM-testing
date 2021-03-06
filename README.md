# Generative Dialogue Model Automatic Quality Assurance tool

## Description   
This is the test framework developed in the Master's Thesis Project *Quality Measurement of Generative Dialogue Models for Language Practice*, conducted at the Computer Science institution at the Faculty of Engineering at Lund University, Sweden.


## How to ...

### ... run the test framework to produce and exports results to the SQLite-file
First, install dependencies   
```bash
# clone project   
git clone https://github.com/JoohanBengtsson/GDM-testing

# install project   
cd GDM-testing
pip install -e .   
pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html
 ```   
 Next, navigate to any file and run it.   
 ```bash

# run module   
python main.py <OPTIONS> [PARAMETERS]    
```
Where several options are available and needed, as to fit your sought for set up of GDMs. Run `python main.py -h` to have the options presented, or read below:

```bash

# options available
usage: main.py [-h] [-l] [-a] [-t] [-cp] [-ec] [-is] [-v] [-cs] [-rf] [-ot]

Parser for setting up the script as you want

optional arguments:
  -h, --help            show this help message and exit
  -l , --length-conv-round
                        How many rounds shall there be per conversation until restart
  -a , --amount-convs   How many conversations shall there be per tested GDM
  -t , --tested-gdms    Write one or several GDMs you want to test. If several, have them separated by ','.
  -cp , --conv-partner
                        Specify which GDM to test your GDM against
  -ec , --export-channel
                        Specify which channel to export the results through. Currently only 'sqlite' is implemented
  -is , --internal-storage
                        Specify which channel to use for the internal storage of results. Currently only 'json' is
                        implemented.
  -v, --verbose         True: The script prints out what happens so that the user may follow the process. False: A
                        silent run of the script where nothing is printed. Defaults to True.
  -cs , --conv-starter
                        Testee: testee initiates every conversation. Conv-partner: the conversation partner initiates
                        all conversations. Not specified: 50-50 per conversation who starts that conversation.
  -rf , --read-file-name
                        The path to the file you want to read into the script. Interprets the letters behind the '.'
                        as the file type. No input is interpreted as such the script generates conversations using the
                        GDMs. Currently only miscellaneous .txt-files are supported.
  -ot, --overwrite-table
                        Should the current table be overwritten or should the results be inserted into the currently
                        existing one. True for creating a new table, False for inserting into the currently existing
                        database-file. Defaults to True.
```

### ... visualise the results from the SQLite-file

1. Install and set up a Grafana-server. More information about that can be found here: https://grafana.com/docs/grafana/latest/setup-grafana/installation/.
2. Hold over the '+'-sign corresponding to the 'Create' menu. In the shown menu, click 'Import'.
3. In the box "Import via panel json", paste in the dashboard-json which can be found in the repository in the file 'dashboard-json.tex', and click load.
4. Then, hold over the 'Gear'-icon on the left to show the "Configuration". There, click "Data sources"
5. There click "Add data source" and add the path to your SQLite-file, which by default is located in your local repository.
6. When you have added the data source, the dashboard should visualise all the implemented test case results. You are also free to make new figures, to which you can fetch data from the SQLite-file by doing SQLite-queries through Grafana.

### Citation   
```
@article{JohanBengtsson2022,
  title={Quality Measurement of Generative Dialogue Models for Language Practice},
  author={Johan Bengtsson},
  year={2022}
}
```   

![](imgs/Test%20architecture.drawio.png)
The proposed architecture as of now for the test framework.

![](imgs/Class%20diagram.drawio.png)

The proposed class diagram for the test framework as of now.

Both are subject to changes.

