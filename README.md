Template for a simple flask project 

To set up:
- clone
- create venv
`python3 -m venv venv`
- activate venv
`. venv/bin/activate`
- install flask
`pip3 install flask`

To run project on local host
`$ python3 run.py`
- when the virtual environment is active 


- document code using pydocs 
    - create docstrings with
    `""" instert description here """`
    - install pdoc 
    `pip3 install pdoc3`
    - create documentation html using the following command
    `pdoc --html <package/directory/filename of project>`
    `pdoc --html src --output-dir docs --skip-errors --force`

- install pytest
`pip install -U pytest`
    - cd into directory of file and run 
    `pytest filename.py` 
    - example of texting = 
    ```def func(x):
        return x + 1


    def test_answer():
        assert func(3) == 5```



deactivate venv before commiting to git etc. 
`deactivate`