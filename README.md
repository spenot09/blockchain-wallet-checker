# Welcome to the Blockchain Wallet Checker
Hacks and other malicious activity are rampant within the DeFi and public blockchain space, leading to significant loss of funds to users. Users should be able to transact freely and with confidence on these public networks, without fear of: 
- scams 
- rug pulls (theft of funds by teams making false promises)
- honeypot contracts (smart contracts that prevent withdrawal of funds, e.g. being able to buy a token but only the development team being able to sell) 
- there are many other forms of malicious activity that target retail and the less sophisticated blockchain users

Blockchain Wallet Checker allows you to verify the safety of a target wallet before you make a transaction on a public blockchain. On the backend, a TigerGraph based graph hosts nodes and transactions which are analysed to identify potentially fraudulent wallets or wallets whose activity may appear suspicious. This is communicated back to the end-user as a score between 0-10 where the higher the score the safer the target wallet is assumed to be.

# Getting started
Before you get started, please reach out to the team to get credentials to be able to access the TigerGraph database so as to allow the scores to be calculated. Without these credentials you will not be able to access the backend, and hence won't be able to use the tool.

## Step 1.
1. Create a new python environment
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
SECRET=<api token>
```

An example `.env.example` is provided with non-genuine credentials.

## Step 3.
Now you can either run the tool via the command line or use the front-end.

**Option 1:** To run with the command line, simply run the following with your target wallet as the input (e.g. `0x4c8945897E306fbE6Dd2d1d3062f33d0eCF753f8`). There is also a network flag that can be used to select various networks in the future. By default this is set to "ethereum":

``` python:
python wallet-checker/check_wallet.py --wallet <target eth wallet address> 
```
To examine the options available as arguments run
``` python:
python wallet-checker/check_wallet.py -h
```

**Option 2:** Or if you prefer to navigate the tool via the front-end simply run the following in your command line (various other terminal options are available here: https://flask.palletsprojects.com/en/2.0.x/quickstart/)

```
set FLASK_APP=walletChecker/app
flask run
```
This will run a host locally on your machine. If you now navigate to http://127.0.0.1:5000/ in your browser you have accessed the front-end of the tool!

Now you can enter your chosen wallet address to receive a score.


