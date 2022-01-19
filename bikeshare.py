import time
import math
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'chi': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'new york city': 'new_york_city.csv',
              'wash': 'washington.csv',
              'washington': 'washington.csv' }
MONTH_DATA = { 'january': 1,
                'jan': 1,
                'february': 2,
                'feb': 2,
                'march': 3,
                'mar': 3,
                'april': 4,
                'apr': 4,
                'may': 5,
                'june': 6,
                'jun': 6}

WEEK_DATA = { 'monday': 0,
                'mon': 0,
                'tuesday': 1,
                'tues': 1,
                'tue': 1,
                'wednesday': 2,
                'wed': 2,
                'thursday': 3,
                'thur': 3,
                'thu': 3,
                'friday': 4,
                'fri': 4,
                'saturday': 5,
                'sat': 5,
                'sunday': 6,
                'sun': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! welcome to bikeshare data')
    wrong_count_city = 0
    wrong_count_month = 0
    wrong_count_day = 0
    collect_inputs = True
    while collect_inputs:
        city = input(f'Attempt #{wrong_count_city+1} Choose a city to check - Chicago/chi/CH, New York City/new york/NY/NYC, or Washington/wash/WA? ').lower()
        if city=='ch':
            city='chicago'
        if city=='ny' or city=='nyc':
            city='new york city'
        if city=='wa' or city=='washington dc' or city=='dc':
            city='washington'
        if city not in CITY_DATA:
            print('Kindly enter a valid city')
            wrong_count_city += 1
            continue
        city = CITY_DATA[city]
        break
    while collect_inputs:
        choice = input('Do you want to filter the data by month or week or both ? Yes/No ').lower()
        if choice=='yes' or choice=='y' or choice=='ok':
            choice=True
        elif choice=='no' or choice=='n' or choice=='nope':
            day='all'
            month='all'
            choice=False
            collect_inputs = False
        else:
            print('Not valid. Enter a valid choice ')
            continue
        break

    while collect_inputs:
        filter=input('You can filter by month / day / both ').lower()
        if filter=='month' or filter=='m':
            print('Which month\'s data to look at?')
            month = input('January/jan, February/feb, March/mar, April/apr, May, June/jun- ').lower()
            if month not in MONTH_DATA:
                print('Invalid input. Could you try again?')
                wrong_count_month += 1
                continue
            month = MONTH_DATA[month]
            day='all'
        elif filter=='day' or filter=='d':
            print('Which day\'s data to look at? ')
            day = input('Monday/mon, Tuesday/tues, Wednesday/wed, Thursday/thur, Friday/fri, Saturday/sat, Sunday/sun- ').lower()
            if day not in WEEK_DATA:
                print('Invalid input. Could you try again?')
                wrong_count_day += 1
                continue
            day = WEEK_DATA[day]
            month='all'
        elif filter=='both' or filter=='b':
            print('Which month\'s data to look at?')
            month = input('January/jan, February/feb, March/mar, April/apr, May, June/jun- ').lower()
            if month not in MONTH_DATA:
                print('Invalid input. Could you try again?')
                wrong_count_month += 1
                continue
            month = MONTH_DATA[month]
            print('And day of the week?')
            day = input('Monday/mon, Tuesday/tues/tue, Wednesday/wed, Thursday/thur/thu, Friday/fri, Saturday/sat, Sunday/sun- ').lower()
            if day not in WEEK_DATA:
                print('Invalid input. Could you try again?')
                wrong_count_day += 1
                continue
            day = WEEK_DATA[day]
        else:
            print('Invalid input. Could you try again?')
            continue
        break
    #Checkout the fun message for total attempts made to enter data
    print(f'City Attempts = {wrong_count_city+1}, Month Attempts = {wrong_count_month+1}, Day Attempts = {wrong_count_day+1}***********************')
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
    df = pd.read_csv(city)
    #extracts and add day_of_week and month from start_time field for each row
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month

    #filters data based upon input day & month
    if day != 'all':
        df = df[df['day_of_week'] == day]
    if month != 'all':
        df = df[df['month'] == month]

    #returns df with two new added columns of month and day_of_week
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # This is to display the most common month
    most_freq_month = df['month'].mode()[0]
    for num in MONTH_DATA:
        if MONTH_DATA[num]==most_freq_month:
            most_freq_month = num.title()
    print(f'The most common month for travel is {most_freq_month}')

    # This is to display the most common day of week
    most_freq_day = df['day_of_week'].mode()[0]
    for num in WEEK_DATA:
        if WEEK_DATA[num]==most_freq_day:
            most_freq_day = num.title()
    print(f'The most common day of week for travel is {most_freq_day}')

    # This is to display the most common start hour
    df['hour']=pd.to_datetime(df['Start Time']).dt.hour
    most_freq_hour = df['hour'].mode()[0]
    print('The most common hour for travel is {}'.format(most_freq_hour))
    #drops the newly added hour column from dataframe
    df.drop('hour',axis=1,inplace=True)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # This is to display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'Most commonly used start station is {common_start_station}')

    # This is to display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'Most commonly used end station as per our data was {common_end_station}')

    # This is to display most frequent combination of start station and end station trip
    start_to_end_station = df['Start Station'] + ' to ' + df['End Station']
    common_start_to_end_station = start_to_end_station.mode()[0]
    print(f'The most frequnt combination of start station and end station trip was {common_start_to_end_station}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    travel_durations = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    # This is to display total travel time
    total_duration_sum = df['Trip Duration'].sum()
    sum_seconds = total_duration_sum%60
    sum_minutes = total_duration_sum//60%60
    sum_hours = total_duration_sum//3600%60
    sum_days = total_duration_sum//24//3600
    print(f'Total travel time all combined was {sum_days} days, {sum_hours} hours, {sum_minutes} minutes and {sum_seconds} seconds')

    # This is to display mean travel time
    total_duration_mean = math.ceil(df['Trip Duration'].mean())
    mean_seconds = total_duration_mean%60
    mean_minutes = total_duration_mean//60%60
    mean_hours = total_duration_mean//3600%60
    mean_days = total_duration_mean//24//3600
    print(f'Mean travel time for all data was {mean_days} days, {mean_hours} hours, {mean_minutes} minutes and {mean_seconds} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # This is to display counts of user types
    user_types = df.groupby('User Type',as_index=False).count()
    print(f'Number of types of users are {len(user_types)}')
    for i in range(len(user_types)):
        print('{}s - {}'.format(user_types['User Type'][i], user_types['Start Time'][i]))

    # This is to display counts of gender
    if 'Gender' not in df:
        print('No gender data found for this city')
    else:
        users_gender = df.groupby('Gender',as_index=False).count()
        print(f'Count of genders of users are {len(users_gender)}')
        for i in range(len(users_gender)):
            print('{}s - {}'.format(users_gender['Gender'][i], users_gender['Start Time'][i]))
        print('Gender data for {} users is not available.'.format(len(df)-users_gender['Start Time'][0]-users_gender['Start Time'][1]))

    # This is to display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('Birth year data is not available for this city')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('Earliest year of birth was {}.'.format(int(birth['Birth Year'].min())))
        print('Most recent year of birth was {}.'.format(int(birth['Birth Year'].max())))
        print('Most common year of birth year was {}.'.format(int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    choice = input('Display source file data ? Yes/No ').lower()
    if choice=='yes' or choice=='y' or choice=='yus':
        choice=True
    elif choice=='no' or choice=='n' or choice=='nope':
        choice=False
    else:
        print('Invalid choice. Try again. ')
        display_data(df)
        return

    display_counter = 0
    if choice:
        while 1:
            for i in range(5):
                print(df.iloc[display_counter])
                display_counter+=1
            choice = input('Display next five? Yes/No ').lower()
            if choice=='yes' or choice=='y' or choice=='yus':
                continue
            elif choice=='no' or choice=='n' or choice=='nope':
                break
            else:
                print('Invalid choice entered')
                return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        #this will retrigger the full code again if yes
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes' and restart != 'y' and restart != 'yus':
            break

if __name__ == "__main__":
	main()
