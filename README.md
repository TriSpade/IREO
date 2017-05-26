IREO (Intelligent River Extreme Orange)
=======================================

Alias: Orange River
===================

Website: https://orangeriver.me

**Introduction:**

IREO or Orange River is a year long project made for CPSC 3990 known as Extreme
Orange. For more information about Extreme Orange see their website at
[http://cybertiger.clemson.edu/eo](http://cybertiger.clemson.edu/eo). This
project is sponsored by IBM, and was made for Intelligent River an ongoing
research project for Clemson University. For more information about Intelligent
River see
[http://www.clemson.edu/centers-institutes/scwater/ir-nsf-mri.html](http://www.clemson.edu/centers-institutes/scwater/ir-nsf-mri.html)
and
[https://www.intelligentriver.org/data](https://www.intelligentriver.org/data).

**Files**

- IR Machine Learning.IPYNB : The Jupyter Notebook file responsible for taking the data from the simulated sensor and then running it       through a simple machine learning algorithm to find outliers.
- README.md : the file you are currently reading which explains how everything works.
- csv_files.tar.gz : This is historical sensor data from actual sensors in the Savana River that is used for this experiment, and outlier   data made to show that the experiment does work.
- iotServer_mysql_to_iot.py : This is a simple Python script that takes WunderGround API historic weather data and the historic data         mentioned previously, merges it and then sends it to the IBM Bluemix IOT Service to act as a simulated sensor for the Jupyter notebook     script.
