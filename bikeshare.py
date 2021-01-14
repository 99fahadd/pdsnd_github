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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to           handle invalid inputs
    # input from the user will be stored in 'city'
    city= ''
    
    while city not in CITY_DATA.keys():
        print('\nWhat city would you like to choose?')
        print("\n1. Chicago 2. New York City 3. Washington")
        # convert the input to lower
        city= input().lower()
        if city not in CITY_DATA.keys():
             print("\nPlease enter a valid input.")  
                
    print("\nYou've choosed {} city.".format(city.title()))
    
    # TO DO: get user input for month (all, january, february, ... , june)
    # MONTH_DATA dictionary stores the months from January to June and month variable stores the inmput coming from the user
    MONTH_DATA= {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month= ''
    
    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month you want to process its data: January, Fabruary, march, april, or June. \nEnter (All) if you want data from all the months.")
        month = input().lower()
        if month not in MONTH_DATA.keys():
             print("\nPlease enter a valid input.")
                
    print("\nYou've choosed {}.".format(month.title()))    
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_LIST= ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day= ''
    
    while day not in DAY_LIST:
        print("\nPlease enter a day of the week of your choice for which you're seeking the data:")
        print("\n(You can also put 'all' or 'All' to view data for all days in a week.)")
        day= input().lower()
        
        if day not in DAY_LIST:
            print("\nPlease enter a valid input.")
    print("\nYou have chosen {} as your day.".format(day.title()))     
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
    
    # casting Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #extract month
    df['month'] = df['Start Time'].dt.month
    
    #extract day of the week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    #Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    #Filter by day of the week
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f"\nMost Popular Day: {popular_day}")

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nMost Popular Start Hour: {}".format(popular_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {common_start_station}")

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"\nThe most commonly used end station: {common_end_station}")
    
    # TO DO: display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]
    print(f"\nThe most frequent combination of trips are from {combo}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("Total trip duration: {} hours, {} minutes and {} seconds.".format(hour,minute,second))
    
    # TO DO: display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nAverage trip duration: {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nAverage trip duration: {mins} minutes and {sec} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print("The types of users by number are given below:\n\n{}".format(user_type))
    

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nThe types of users by gender are given below:\n\n{}".format(gender))
    except:
        print("\nThere is no 'Gender' column in this file.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth: {}\n\nThe most recent year of birth: {}\n\nThe most common year of birth: {}".format(earliest, recent, common_year))
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Asks if the user wants to see the raw data and display 5 rows for every request
    
        Args:
        param1 (df): The data frame you wish to work with.
        
        Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nWould you like to view the raw data?(yes/no)")
        rdata = input().lower()
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nInvalid input.")
    
    while rdata == 'yes':
        print("Would you like to view the more raw data?(yes/no)")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break
    
    print('-'*40)
              

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
