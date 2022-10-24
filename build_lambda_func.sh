# Download the data files
cd data
wget https://correlatesofwar.org/wp-content/uploads/dyadic_mid_4.01.zip
unzip dyadic_mid_4.01.zip
wget https://correlatesofwar.org/wp-content/uploads/COW-country-codes.csv
cd ..

# Create a zip file to upload to AWS
zip -r lambda_function.zip . -x "venv/*" -x "__pycache__/*" -x ".idea/*" -x ".git/*"

