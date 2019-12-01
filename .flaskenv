FLASK_APP=comparenba.py

#development
DEV_POSTGRES_URL=localhost
DEV_POSTGRES_USER=rodrigocuriel
DEV_POSTGRES_PW=""
DEV_POSTGRES_DB=champion

#testing
export TESTING_POSTGRES_URL="localhost"
export TESTING_POSTGRES_USER="rodrigocuriel"
export TESTING_POSTGRES_PW=""
export TESTING_POSTGRES_DB="test_db"

#production
export PROD_POSTGRES_URL="ec2-107-20-168-237.compute-1.amazonaws.com"
export PROD_POSTGRES_USER="rltvjaswjfyvfb"
export PROD_POSTGRES_PW="3fe3fd924b885bcc92434654100df16abc10b0a8cc4b4a07a0083a1d17ac62f1"
export PROD_POSTGRES_DB="dd3143fukofoto"