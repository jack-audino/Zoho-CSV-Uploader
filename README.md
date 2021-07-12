# Zoho-CSV-Uploader
A tool used to parse CSV files containing client data and upload it to Zoho using the API

# How to use:
  1. **Create a Self-Client and Grant Token using the [Zoho API Console](https://api-console.zoho.com/)**
  		* Press ```GET STARTED``` and on the subsequent screen, select the ```CREATE NOW``` option for ```Self-Client```
  			![Screenshot2](https://user-images.githubusercontent.com/87036127/124659060-87263c00-de72-11eb-91c2-017cfb618cd7.png)
		* Upon doing so, you will be prompted to create the the Self-Client and then to confirm this action
		* After creating your client, you will be presented with the ```Client ID``` and the ```Client Secret``` (these will be used later)
  			![Screenshot3](https://user-images.githubusercontent.com/87036127/124660358-197b0f80-de74-11eb-9bdb-6b390ae8d1b7.png)
		* Now, a Grant Token must be generated (which will also be needed later) by switching to the ```Generate Code``` tab above the client information
		* In this tab, you are required to give a scope, which will be ```aaaserver.profile.ALL, ZohoCRM.modules.leads.CREATE``` (since the tool is used to create client leads) a time duration, and a scope description, which in this case will be 'Uploading lead information'<br/>
			![Screenshot4](https://user-images.githubusercontent.com/87036127/124661798-00735e00-de76-11eb-9eda-7413038ea303.png)
		* Upon hitting ```CREATE``` you will be sent to a new page which prompts you to choose a ```Portal```, which in this case should be ```CRM``` since that is the desired destination for the leads, and a ```Production``` which will be the company or organization that you have created your Zoho account for
			![Screenshot5](https://user-images.githubusercontent.com/87036127/124662422-d1a9b780-de76-11eb-832f-96061dacaa40.png)
		* After entering your ```Portal``` and ```Production```, scroll down and press ```CREATE```, and you will be presented with your Grant Token which will only be valid for the duration that you chose
			![Screenshot6](https://user-images.githubusercontent.com/87036127/124663075-9c519980-de77-11eb-8295-aead945d8ad1.png)
			
  2. **Run the Executable File**
		* After running the executable, open the Developer Window using the ```Open Developer Window``` button
			![Screenshot7](https://user-images.githubusercontent.com/87036127/124664217-1e8e8d80-de79-11eb-8a86-ed0295ea2a28.png)
		* Once you are in the Developer Window, open the Configuration Window using the ```Open Config Window``` button
			![Screenshot8](https://user-images.githubusercontent.com/87036127/124665393-aa54e980-de7a-11eb-8c99-d01670511040.png)
		* In the Configuration Window, enter the ```Client ID```,```Client Secret``` and ```Grant Token``` in their respective places
			![Screenshot9](https://user-images.githubusercontent.com/87036127/124666208-b4c3b300-de7b-11eb-9751-7f2a83a63148.png)
		* Then, exit the Configuration Window, and in the Developer Window, generate new ```Access```, ```Refresh``` and ```Refresh-Generated Access``` Tokens by using the ```Use Grant Token``` button
		* After doing so, re-open the Configuration Window, and you should now see that at the bottom, there are now newly-generated tokens, meaning you can now upload CSV files to Zoho
			![Screenshot11](https://user-images.githubusercontent.com/87036127/124667342-467ff000-de7d-11eb-8302-0939a34f751c.png)  	
  3. **Parsing and Uploading Your CSV File**
  		* Before uploading your CSV file containing your client information, ensure that it is formatted like the CSV file below (this file can be found in ```/CSV File Examples```)
  			![Screenshot12](https://user-images.githubusercontent.com/87036127/124668161-72e83c00-de7e-11eb-8f93-6e6c1b579588.png)
		* Additionally, ensure that any and all titles (i.e. any word that's in the first row) are in the following keyword list (this list can be found in ```csv_parser.py```)<br/>
			![Screenshot13](https://user-images.githubusercontent.com/87036127/124668299-a6c36180-de7e-11eb-880f-0933ac43476f.png)
		* Finally, once you are sure that your CSV file is properly-formatted, go to the main window, select the ```Select a file to upload to Zoho``` button, find the location of your desired CSV file, and if it is sent to Zoho and the API accepts it, you should receive the following pop-up message<br/>
			![Screenshot14](https://user-images.githubusercontent.com/87036127/124669506-7c72a380-de80-11eb-96d8-b1e9c15d77bd.png)
		* To confirm that your leads page has been updated, check your leads page in your Zoho CRM, and you should see them uploaded (these clients were made using ```/CSV File Examples/csv_file_1.csv```)
			![Screenshot15](https://user-images.githubusercontent.com/87036127/124669733-dffcd100-de80-11eb-9f5b-441e1f2a6a98.png)
		* You can also check to ensure that each client was uploaded with the proper information from the csv file
			![Screenshot16](https://user-images.githubusercontent.com/87036127/125352130-e41c6900-e32e-11eb-96b6-2a197c7bd8dc.png)

