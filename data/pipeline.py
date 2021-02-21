from package import MotorScraper
import pandas as pd


def get_data() -> pd.DataFrame:
    """
    Get data in a DataFrame by using the MotorScraper package to scrape autoscout.nl
    :return: pd.DataFrame
    """
    list_try = MotorScraper().collect_urls(20, ['kawasaki', 'honda', 'bmw', 'yamaha', 'ducati'])
    df = MotorScraper().collect_info(list_try)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data
    :param df: the DataFrame to be cleaned
    :return: pd.DataFrame
    """
    for column in df.columns:
        df[column] = df[column].str.replace('.', '')
        df[column] = df[column].str.replace('\n', '')
        if column == 'price':
            df.price = df.price.str.extract(r'(\d+)')
        elif column == 'cc':
            df.cc = df.cc.str.extract(r'(\d+)')
        elif column == 'power':
            df.power = df.power.str.extract(r'(\d+)')
        elif column == 'mileage':
            df.mileage = df.mileage.str.extract(r'(\d+)')
    return df


def set_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Set data types of the dataframe
    :param df: The dataframe to be changed
    :return: pd.DataFrame
    """
    df[["price", "mileage", "power", "cc", "year"]] = \
        df[["price", "mileage", "power", "cc", "year"]].apply(pd.to_numeric)
    return df


def preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle null values and prepare the dataframe for the model
    :param df: the dataframe to be preprocessed
    :return: pd.DataFrame
    """
    df.dropna(subset=['brand'], inplace=True)
    df.new.fillna("Not defined", inplace=True)
    df['mileage'][df.new == "Nieuw"] = 0
    df.fuel.fillna("Not defined", inplace=True)
    df.year.fillna(df.year.mean(), inplace=True)
    df.cc.fillna(df.cc.mean(), inplace=True)
    df.power.fillna(df.power.mean(), inplace=True)
    df.mileage.fillna(df.mileage.mean(), inplace=True)
    df.round(2)
    return df


def write_csv(df: pd.DataFrame):
    """ Write the dataframe to a csv file """
    df.to_csv('data.csv', index=False)


def pipeline() -> str:
    """
    Run all the tasks in the pipeline to process the data
    :return: String
    """
    df = get_data()
    cleaned_data = clean_data(df)
    final_df = set_data_types(cleaned_data)
    processed = preprocessing(final_df)
    write_csv(processed)
    return "All done"
