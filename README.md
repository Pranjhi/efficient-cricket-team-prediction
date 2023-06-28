# Making Dream Team
## Objective
The objective is to use linear programming in a real world application.<br>
We are trying to make a team that satifies all the constrain and maximise the total expected points<br>

## Compile
Make sure to have pulp library installed<br>
To install pulp do:<br>
```
pip install pulp
```
After that run the following steps:<br>
```
git clone git@github.com:Aditya-debug15/Fantasy-Cricket-team-selection.git
cd Fantasy-Cricket-team-selection
python dreamteam.py
```
<br>
Instead of using `python/pip` you can use `python3/pip3`<br>
After running the above command terminal will look like:<br>
<img src="screenshots/1.jpg"><br>

For the input give the filelocation it accepts both relative and absolute path<br>
The output will be available in `Outputs/results_filename` from where you have executed the code<br>

Sample input file must look like this:<br>
<img src="screenshots/2.jpg"><br>
Output file will contain the players<br>
Along with selected players,the choice of captain and vice captain will be printed on terminal<br>
<img src="screenshots/3.jpg"><br>