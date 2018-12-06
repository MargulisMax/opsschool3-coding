node ('OpsSchool-Dynamic-Slave'){
   stage('aaaa'){
       sh 'echo "stage one"'
       dir('weather'){
           git url: 'https://github.com/MargulisMax/opsschool3-coding.git'
       }
   }
   sh '''
       python3.7 ../../.local/bin/pip install --user click weather-api
       cd weather/home-assignments/session2/
       python3.7 cli.py --city dublin --forecast TODAY -c
   '''