openweather.py interface

  Interface for choosing countries with pagination. The program prints a list of countries
    <Country code>, <Country name> devided into pages.
    User can getting through pages via commands:
    -n next page
    -p previous page
    -e exit
    User choose the country and put its CODE into input line.
    
    
Interface for choosing cities with pagination and filtering. The program prints a list of cities
<city id>, <city name> devided into pages.
User can getting through pages via commands:
-n next page
-p previous page
-e exit

User can insert only begining of city name (like mos for Moscow) and the program will print
consequent list of cities.

-ms brings the city list to the initial state (Whole city list) to begin new search

User choose the city and put its ID into input line.

After User has finished choosing city of a current country, enter -e to go to the NEXT country
city chose.
