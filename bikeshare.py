import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
DAYS ={
0: "monday",
1: "tuesday",
2: "wednesday",
3: "thursday",
4: "friday",
5: "saturday",
6: "sunday"
}
MONTHS={
1:"january",
2:"february",
3:"march",
4:'april',
5:'may',
6:'june',
7:'july',
8:'august',
9:'september',
10:'october',
11:'november',
12:'december'
}

def select_city():
    """
    Provides the users with the list of available cities and prompts them to select one for analysis.

    Returns:
        (str) city - name of the city to analyze
    """
    print('Welcome! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while 1:
        print('\n Please select a city of interest from the following list:')
        for key in CITY_DATA:
            print(key.title())
        city = input().lower()
        if city in CITY_DATA:
            break
        print("\n Oops! That's not an included city.")
    return city

def load_data(city):
    """
    Loads data for the specified city.

    Args:
        (str) city - name of the city to analyze

    Returns:
        df - Pandas DataFrame containing city data
    """
    print("\nLoading",city,"data...\n")
    df=pd.read_csv(CITY_DATA[city])
    print(city,"data loaded")
    print('-'*40,"\n")
    return df

def extract_cols(df):
    """
    Creates DateTime and trip columns. Remaps days and month columns from integer index to strings

    Inputs:
        Pandas.dataframe - The raw dataframe of the selected city
    Returns:
        Pandas.dataframe - The dataframe of the selected city with additional time and trip columns
    """
     # extract month, day of week and hour from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] =df['Start Time'].dt.hour

    #create a column to describe trip start to end
    df["trip"] = df["Start Station"] + " -> " + df["End Station"]

    #remap number index in ['months'] to strings
    df['month']=df['month'].map(MONTHS)

    #remap number index values in ['day of week'] to strings
    df['day_of_week'] = df['day_of_week'].map(DAYS)

    return df

def get_filters(df):
    '''
    Presents a list of unique months for user filtering.
    Asks user to specify month and day to analyze.
    Applies these filters to the dataframe

    Inputs:
        Pandas.dataframe - The unfiltered dataframe of the selected city
    Returns:
        Pandas.dataframe - The dataframe of the selected city
    '''
# print a list of months for the user to select from and get user input for month (all, january, february, ... , june)
    while 1:
        print("Please choose a month to examine from the list below, or select 'all' to include all months.")
        print(df['month'].unique())
        try:
            user_month=input().lower()
            if user_month == "all":
                break
            elif user_month in df["month"].values:
                break
            else:
                print("\n Oops! that's not a month included in the dataset.\n\n")

        except:
            print("\n Oops! Please enter a listed month as a number or 'all'.\n\n")

    # a failure message for unaticipated day input
    day_failure='''\n Oops! you didnt select a day of the week. Please choose from: \n
    'monday','tuesday','wednesday','thursday','friday','saturday','sunday' or 'all'
    '''

    print(('-'*40),"\n")
    while 1:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        print("Please choose a day of the week to examine from the list below, or select 'all' to include all days")
        print(df['day_of_week'].unique())
        try:
            user_day=input().lower()
            if user_day=="all":
                break
            elif user_day in df["day_of_week"].values:
                break
            else:
                print(day_failure)
        except:
            print(day_failure)
    print('-'*40)
     # filter by month to create the new dataframe
    if user_month != 'all':
        print("user month is:", user_month)
        df = df[df.month == (user_month)]
    if user_day != 'all':
        print("user_day is:", user_day)
        df = df[df.day_of_week == user_day]
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most popular month to travel is {}".format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day of the week to travel is {}".format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular hour to travel is {}:00".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("The most popular starting station is {}".format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("The most popular ending station is {}".format(popular_end))



    # display most frequent combination of start station and end station trip
    popular_trip = df["trip"].mode()[0]
    print("the most common start station to end station trip is {}".format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    totalseconds=df["Trip Duration"].sum()

    totaldays=(totalseconds//(60*60*24))
    remainder=totalseconds-(totaldays*60*60*24)

    totalhours=remainder//(60*60)
    remainder-= totalhours*60*60

    totalminutes=remainder//60
    remainder-= (totalminutes*60)
    remainder=int(remainder)

    print("""Total travel time by all users was:\n
    {} day(s), {} hour(s), {} minutes(s) and {} second(s)
    """.format(totaldays,totalhours,totalminutes,remainder))

    # display mean travel time
    meantravel=df['Trip Duration'].mean()
    meanminutes=int(meantravel//60)
    meanremainder=int(meantravel-(meanminutes*60))
    print("The average trip was {} minutes and {} second(s)".format(meanminutes,meanremainder))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        usercount=df.groupby(['User Type']).size()

        print(usercount.to_string(),"\n")

    # Display counts of gender
    except:
        print("User type data is unavailable for this city")


    try:
        gendercount=df.groupby(['Gender']).size()

        print(gendercount.to_string(),"\n")
    except:
        print("User gender data is unavailable for this city")

    # Display earliest, most recent, and most common year of birth
    try:
        earliestbirth = int(df['Birth Year'].min())
        print("The earliest birth year is {}.\n".format(earliestbirth))

        latestbirth = int(df['Birth Year'].max())
        print("The most recent birth year is {}.\n".format(latestbirth))

        commonbirth = int(df['Birth Year'].mode()[0])
        print("The most common birth year is {}.\n".format(commonbirth))

    except:
        print('User age data is unavailable for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """shows the user five lines of the dataframe and then prompts them if they
    would like to see more.

    Input: the pandas data frame to be shown"""

    i=0
    while 1:
        stop=i+5
        print(df[i:stop])
        i+=5
        fivemore=input("Would you like to see 5 more rows? Enter 'yes' or 'y' to view more rows: \n")
        try:
            if fivemore.lower()=="yes" or fivemore.lower()=="y":
                continue
            else:
                break
        except:
            break
    print('Exiting data view \n','-'*40)


def main():
    while True:
        city = select_city()
        df = load_data(city)
        df = extract_cols(df)
        filtered_df = get_filters(df)

        time_stats(filtered_df)
        station_stats(filtered_df)
        trip_duration_stats(filtered_df)
        user_stats(filtered_df)
        while 1:
            prompt_failure="Please enter 'yes' or 'no'\n"
            try:
                data_prompt=input("""
Would you like to see the first five rows of raw data? Enter 'yes' to see the data or 'no' so skip. \n
                """).lower()
                if data_prompt == "yes":
                    show_data(filtered_df)
                    break
                elif data_prompt == "no":
                    break
                else:
                    print(prompt_failure)
            except:
                print(prompt_failure)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
