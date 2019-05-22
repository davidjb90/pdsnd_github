import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #  user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        i = input("\nWhat city would you like to explore? We can tell you about Washington, New York City, or Chicago. Please enter the name of one of these cities: ").lower()
        city = i
        if city in CITY_DATA:
            print('\nGreat! ' + city[0].upper() + city[1:] + ' is a super groovy city that likes to share!\n')
            break
        print("\nSorry, but you gotta choose a city... Please check your spelling if you already chose...\n")
    #  user input for month (all, january, february, ... , june)
    while True:
        month_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
        time_input = input("Do you have specific month you would like to see? type Y/N: ").lower()
        if time_input == "y": 
            month_input = input("\nOk, please type the month: ").lower()
            ### Adding functionality to enter mixed/uppercase month
            if month_input in month_list:
                month = month_input
                break
            if month_input not in month_list:
                print("\nSorry but please check your spelling...\n")
        elif time_input == 'n':
                month = "all"
                break
        else:
            print("\nSorry but you must type 'y' or 'n'\n")
    #  user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        time_prompt = input("\nDo you have specific day you would like to see? type Y/N: ").lower()
        if time_prompt == "y": 
            day_input = input("\nOk, please type the day: ").lower()
            ### Adding functionality to enter mixed/uppercase day
            if day_input in day_list:
                day = day_input
                break
            if day_input not in day_list:
                print("\nSorry but please check your spelling...\n")
        elif time_prompt == 'n':
                day = "all"
                break
        else:
            print("\nSorry but you must type 'y' or 'n'")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
            month = months.index(month) + 1

        # filter by month to create the new dataframe
            df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # define and print most common month
   
    month_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    popular_month = df['month'].mode()[0]
    month = month_list[popular_month - 1]
    print("The most frequent bikesharing month is: " + month[0].upper() + month[1:])
    
    # define and print most common day of week
    
    day = df['day_of_week'].mode()[0]
    print("\nThe most popular day is: " + day)

    # define and print most common start hour
    
    df['Start Hour'] = pd.to_datetime(df['Start Time']).dt.hour
    Common_start_hour = df['Start Hour'].mode()[0]
    print("\nThe most common start hour is: " + str(Common_start_hour) + "00 hrs")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # define and print most commonly used start station
    
    start_station = df['Start Station'].mode()[0]
    print("The most popular start station is: " + start_station)
    
    # define and print commonly used end station
    
    end_station = df['End Station'].mode()[0]
    print("\nThe most popular end station is: " + end_station)

    # Create combo variable and print output
    
    ## New column in dataframe to link the start/end stations as trips
    df['Combo Stations'] = (df['Start Station'] + ' to ' + df['End Station'])
    combo_station = df['Combo Stations'].mode()[0]
    print('\nThe most popular trip is: ' + combo_station)
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # define and print total trip duration variable
    travel_time = df['Trip Duration'].sum()
    print('The total time traveled was: ' + str(travel_time) + ' seconds')

    # define and print average trip duration variable
    avg_time = df['Trip Duration'].mean()
    print('\nThe average trip time was: ' + str(avg_time) + ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    # added city argument to function in order to conditionally display gender/birth year data
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Define user variables and print statistic
    user_counts = df['User Type'].value_counts()
    print("Here are the numbers for the different types of user: ", user_counts)

    # Defining variables for counts of gender
    
    ## try/except clause prevents key error for any datasets that don't have gender/birthyear columns (i.e. Washington)
    try:    
        if city == 'new york city' or 'chicago':
            gender_counts = df['Gender'].value_counts()
            print("\nHere is the breakdown of genders: ", gender_counts)

    # defining variables and print earliest, most recent, and most common year of birth
            earliest_birth = df['Birth Year'].min()
            print("\nThe earliest birth year was: ", int(earliest_birth))
        
            latest_birth = df['Birth Year'].max()
            print("\nThe latest birth year was: ", int(latest_birth))
        
            popular_birth = df['Birth Year'].mode()
            print("\nThe most common birth year was: ", int(popular_birth))
    except: 
        print("\nSorry no gender/birth data for this city.")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    first_row = 0
    last_row = 5
    ask = input("\nDo you want to see the first five lines of raw data? Enter Y/N: ")
    while True:
        row = df.iloc[first_row:last_row]
        if ask.lower() == 'y':
            first_row += 5
            last_row += 5
            print(row)
        else:
            print('\nOk\n')
            break
    
        ask = input("\nDo you want to see the next five lines of raw data? Enter Y/N: ")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Checking if we have data on the entered time frame (no trips in any city July-December)
        # Left functionality for any month in case the dataset were to change
       
        if df.empty:
            print("\nSorry, no trips were taken during that time!\n")
            print('-'*40)
            continue
        
        ### display raw data for statistics 
        raw_data(df)
        # calling statistical functions    
        #### user input for time statistics
        time_stats_input = input("\nWould you like to see the time stats? type Y/N: \n").lower()
        if time_stats_input == "y":
            time_stats(df)
        else: 
            print("\nOk\n")
        #### user input for station statistics
        station_stats_input = input("\nWould you like to see the station stats? type Y/N: \n").lower()
        if station_stats_input == "y":
            station_stats(df)
        else: 
            print("\nOk\n")
        #### user input for trip duration statistics
        trip_stats_input = input("\nWould you like to see the trip duration stats? type Y/N: \n").lower()
        if trip_stats_input == "y":
            trip_duration_stats(df)
        else: 
            print("\nOk\n")
        ######## user input for demographic statistics
        # added city argument to user_stats function in order to conditionally display gender/birth year data
        user_stats_input = input("\nWould you like to see the user stats? type Y/N: \n").lower()
        if user_stats_input == "y":
            user_stats(df, city)
        else: 
            print("\nOk\n")
       
        
        ## Allows the user to rerun without restarting program from terminal
        restart = input('\nWould you like to restart? Type Y/N.\n').lower()
        if restart != 'y':
            break
        if restart == 'y':
            continue

if __name__ == "__main__":
	main()
