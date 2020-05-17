############################################################
#   For <access_key_id>, <secret_access_key> keys, email:  #
#   1) arka.nayak@gmail.com                                #
#   2) arjun.shivraj@steel-eye.com                         # 
############################################################




Steps followed for framing the solution:
-----------------------------------------
1) Create a AWS account
2) Create a IAM role and generate keys
3) Create a AWS lambda function: 'SteelEye'
4) Create a s3 bucket: 'arkas3b'
5) Give access to lambda 'SteelEye' from s3 bucket policy
6) Give access to s3 bucket 'arkas3b' from lambda role policy
7) lambda_function.py contains the logic ('SteelEye' contents in AWS)
8) trigger_lambda.py contains logic to invoke the lambda from terminal
9) check_s3_file_contents.py contains logic to list the contents of s3 bucket


Steps to test:
--------------
1) In  " ~/.aws/credentials " in your local, paste the following 
[default]
aws_access_key_id = <access_key_id>
aws_secret_access_key = <secret_access_key>

2) Run " python3 trigger_lambda.py " to trigger the lambda file

3)  Run " python3 check_s3_file_contents.py " to list the contents of s3 bucket.
    Csv file ( <month_day_year_hour_minute_sec>.csv format ) is generated when the lambda is invoked

P.S.- Regarding point 4) Convert the contents of the xml into a CSV:
        ** Was not able to come up with a solution for this **
