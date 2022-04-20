# Welcome to the Blockchain Wallet Checker
Hacks and other malicious activity are rampant within the DeFi and public blockchain space, leading to significant loss of funds to users. Users should be able to transact freely and with confidence on these public networks, without fear of: 
- scams 
- rug pulls (theft of funds by teams making false promises)
- honeypot contracts (smart contracts that prevent withdrawal of funds, e.g. being able to buy a token but only the development team being able to sell) 
- there are many other forms of malicious activity that target retail and the less sophisticated blockchain users

Blockchain Wallet Checker allows you to verify the safety of a target wallet before you make a transaction on a public blockchain. On the backend, a TigerGraph based graph hosts nodes and transactions which are analysed to identify potentially fraudulent wallets or wallets whose activity may appear suspicious. This is communicated back to the end-user as a score where the higher the score the safer the target wallet is assumed to be.

This score is determined by a custom centrality algorithm that was designed after discovering a correlation  between healthy wallet activity on a network and its trustworthiness. After experimenting with several prebuilt solutions such as Eigen Vectors, Harmonic Centrality, and Page Rank amongst others, this correlated relationship is captured by examining the Degree of a specific target wallet within the network (currently Ethereum only but with scope to easily expand this).

# Getting started
Before you get started, please reach out to the team to get credentials to be able to access the TigerGraph database so as to allow the scores to be calculated. Without these credentials you will not be able to access the backend, and hence won't be able to use the tool.

Ensure you have Microsoft C++ Build Tools installed (which can be installed here https://visualstudio.microsoft.com/visual-cpp-build-tools/) as some of the python libraries require it, otherwise you may have an error:

```
Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

Please note, the below assumes that you already have the required data downloaded that will be loaded into the graph (currently the first couple million transactions on the Ethereum network). The base repo which has been forked contains instructions on how this data can be retrieved (https://github.com/blockchain-etl/ethereum-etl). For demo purposes, a sample dataset has been provided within this repo under `sample/`. However, using our default solution will already have the graph pre-configured.

## Step 1.
1. Create a new python environment (for venv: https://python.land/virtual-environments/virtualenv, for conda: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
2. Clone this repository 
3. Navigate to the root of the repo
4. Install all requirements. 

```ps: 
pip install -r requirements.txt
```

## Step 2.
Now within the root create a new file called `.env`  (literally just .env). Within here add the following and replace with the previously requested credentials:

```
TG_USERNAME=<username>
TG_PASSWORD=<password>
SECRET_ETH_GRAPH=<secret token>
SECRET_KMTEST_GRAPH=<secret token>
```

An example `.env.example` is provided with non-genuine credentials.

## Step 3.
Ensure the TigerGraph Cloud solution is running. Without this activation, the Wallet Checker tool won't be able to connect. By default, the solution will shut down after several hours of inactivity in order to save AWS resources.

To activate the solution:
1. Go to https://tgcloud.io/
2. Ask the team for log in credentials to log into the team portal
3. Navigate to *My Solutions* on the right-hand side panel
4. For the *Blockchain Challenge* project, under the *Actions* column select the *Solution Operations* icon and hit *Start*

The project is now running and is ready to accept external requests.

Project details:
### Network Information
- VPC: vpc-0e629fa9fb3fc8079
- Subnet: subnet-0b34ce547aa169589
- CIDR: N/A
- Domain: 5dab72d8cab74eaabdeac665cf8a72e3.i.tgcloud.io

### Other Information
- Solution ID: aae59fa5-7a95-4c8b-9723-c0aea8daa718
- TigerGraph Version: 3.5.0
- Description: N/A

## Step 4.
Now you can either run the tool via the command line or use the front-end.

**Option 1:** To run with the command line, simply run the following with your target wallet as the input (e.g. `0x4c8945897E306fbE6Dd2d1d3062f33d0eCF753f8`). The query that will return the score is being explicitly set in order to allow future queries that calculate various scores to be implemented with ease. There is also a network flag that can be used to select various networks in the future. By default this is set to "ethereum":

``` python:
python wallet-checker/check_wallet.py --wallet <target eth wallet address> --query WalletScore_Query --network ethereum
```

Example wallets to try (currently due to cloud storage restraints only a subset of the Ethereum blockchain could be loaded in):
- 0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5
- 0x1dcb8d1f0fcc8cbc8c2d76528e877f915e299fbe
- 0x63a9975ba31b0b9626b34300f7f627147df1f526

To examine the options available as arguments run
``` python:
python wallet-checker/check_wallet.py -h
```

**Option 2:** Or if you prefer to navigate the tool via the front-end simply run the following in your command line (various other terminal options are available here: https://flask.palletsprojects.com/en/2.0.x/quickstart/)

```
set FLASK_APP=wallet-checker/application
flask run
```
This will run a host locally on your machine. If you now navigate to http://127.0.0.1:5000/ in your browser you have accessed the front-end of the tool!

Now you can enter your chosen wallet address to receive a score.



