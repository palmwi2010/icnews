# ICNews

## Usage

Steps to run a local version of ICNews

#### Clone the repository
```
git clone git@github.com:palmwi2010/icnews.git
```

#### Create and activate a venv
```
python -m venv venv
source venv/bin/activate
```
#### Install packages
```
pip install -r requirements.txt
```

#### Create a branch
```
git checkout -b [branch_name]
```

#### Run on a local server
```
flask run --debug
```

#### Install pre commit for format checking
```
pre-commit install
```

#### When pushing to remote, set an upstream branch like the below
```
git push -u origin [branch_name]
```
