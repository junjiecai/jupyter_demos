import decimal
from string import ascii_uppercase

import pandas as pd
from pandas import DataFrame, Series


class Const:
    num_to_alphabet = dict(zip([str(i) for i in range(1, 27)], ascii_uppercase))


def null_rate(s):
    return (s.isnull().sum()) / len(s)


def q25(s):
    return s.quantile(0.25)


def median(s):
    return s.quantile(0.50)


def q75(s):
    return s.quantile(0.75)


def nunique(s):
    return s.nunique()


def uniques(s):
    return list(dict(s.value_counts()).keys())


def true_rate(s):
    result = s.sum() / len(s)
    return result


def false_rate(s):
    count = s.value_counts(dropna=True)
    if len(count) == 2:
        result = (s.value_counts(dropna=True)[0]) / len(s)
    else:
        result = 0

    return result


def numerical_distribution(s, cutting_points):
    nmax = s.max()
    nmin = s.min()
    if nmax == nmin or cutting_points or (pd.isnull(nmax) and pd.isnull(nmin)):
        distribution = {'distribute': pd.cut(s, 5).value_counts(True, dropna=False), }
    else:
        cutting_points = get_cutting_point(nmax, nmin)
        distribution = {
            'distribute': pd.cut(s, pd.IntervalIndex.from_tuples(cutting_points)).value_counts(True,
                                                                                               dropna=False), }
    distribution['distribute'] = distribution['distribute'].sort_index()

    return distribution


def categorical_distribution(s):
    dist = s.value_counts(normalize=True, dropna=False).to_dict()
    return dist


def nunique(s):
    return s.nunique()


def get_cutting_point(max, min):
    m = 0
    while max - min < 25:
        m -= 1
        max *= 10
        min *= 10

    if decimal.Decimal(str(max)) % 1 != 0:
        max = max // 1 + 1
    if decimal.Decimal(str(min)) % 1 != 0:
        min = min // 1
    try:
        x = [max + i for i in range(5) if (max + i) % 5 == 0][0]
        y = [min - i for i in range(5) if (min - i) % 5 == 0][0]
    except:
        print(x, y)
    for i in range(5, 11):
        n = (x - y) / i
        if n % 5 == 0:
            break
    if decimal.Decimal(str(n)) % 1 != 0:
        n = n // 1 + 1
        n = [int(n) + i for i in range(5) if (int(n) + i) % 5 == 0][0]
    start = y
    data_list = []
    end = start
    while end < x:
        end = start + n
        if m != 0:
            data_list.append((round(start * (10 ** m), -m), round(end * (10 ** m), -m)))
        else:
            data_list.append((int(start), int(end)))
        start = end

    return data_list


def get_majority(df, group_cols, percentage_threshold=1, n_threshold=10):
    target = df.columns[0]
    len_df = df.groupby(group_cols)[target].agg(len).reset_index().rename(columns={target: 'count'})
    len_df['percentage'] = len_df['count'] / len_df['count'].sum()
    len_df = len_df.sort_values('percentage', ascending=False)
    len_df['percentage'] = len_df['percentage'].cumsum()
    len_df = len_df.rename(columns={'percentage': 'cum_percentage'})

    len_df['type'] = None

    n = len(df[group_cols].drop_duplicates())
    is_minor = (len_df['cum_percentage'] > percentage_threshold) & (n > n_threshold)
    len_df.loc[~is_minor, 'type'] = 'major'
    len_df.loc[is_minor, 'type'] = 'minor'

    return len_df


def bool_summarize(df):
    bool_summary = df.agg(

        [false_rate, null_rate, true_rate])
    return bool_summary.T


def categorical_summarize(df):
    categorical_summary = df.agg([null_rate, nunique])
    categorical_summary = categorical_summary.T
    cate_dict = df.agg(categorical_distribution).to_dict()
    series_list = []
    for cate in cate_dict.keys():
        cate_df = DataFrame(Series(cate_dict[cate]).astype('str')).reset_index()
        cate_df.insert(0, 'feature_name', cate)
        cate_df.rename(index=str, columns={0: 'distribution', 'index': 'category'}, inplace=True)
        series_list.append(cate_df)
    return categorical_summary, series_list


def numerical_summarize(df_numerical, cutting_points):
    numerical_summary = df_numerical.agg(
        [lambda s: numerical_distribution(s, cutting_points), null_rate, min, q25, 'mean', median, q75, max])
    numerical_summary = numerical_summary.T
    nume_dict = numerical_summary['<lambda>'].to_dict()
    numerical_summary.drop('<lambda>', axis=1, inplace=True)
    series_list = []
    for nume in nume_dict.keys():
        nume_df = nume_dict[nume]['distribute'].reset_index()
        nume_df.insert(0, 'feature_name', nume)
        nume_df['index'] = nume_df['index'].astype('str')
        nume_df.rename(index=str, columns={nume: 'distribution', 'index': 'category'}, inplace=True)
        series_list.append(nume_df)
    return numerical_summary, series_list


def get_most_value(df):
    s1 = df.loc[df['distribution'] == df['distribution'].max()]
    s2 = df.loc[df['distribution'] != s1.iloc[0]['distribution']]
    s3 = s2.loc[s2['distribution'] == s2['distribution'].max()]
    s1.rename(index=str, columns={'distribution': 'first_most_value_percentage', 'category': 'first_most_value'},
              inplace=True)
    s3.rename(index=str, columns={'distribution': 'second_most_value_percentage', 'category': 'second_most_value'},
              inplace=True)
    if len(s3) != 0:
        s1 = pd.concat([s1, s3], axis=1)
        return s1.iloc[0]


def summarize(df, output_path, cutting_points=None, config=None):
    date_cols = df.select_dtypes(include=['datetime64'])
    if len(date_cols.columns) != 0:
        df = df.drop(date_cols.columns, axis=1)
    if config:
        # if 'booleans' in config.keys() and 'category' in config.keys():
        bool_summary = bool_summarize(df[config['booleans']])
        categorical_summary, categorical_list = categorical_summarize(df[config['category']])
        df_numerical = df.drop(columns=config['booleans'])
        numerical_cols = df_numerical.drop(columns=config['category'])
    else:
        bool_cols = df.select_dtypes(include=['bool'])
        category_cols = df.select_dtypes(include=['category', 'object'])
        numerical_cols = df.select_dtypes(include=['float64', 'int64'])

        if len(bool_cols.columns) != 0:
            bool_summary = bool_summarize(bool_cols)
        else:
            bool_summary = DataFrame({})
        categorical_summary, categorical_list = categorical_summarize(category_cols)
    numerical_summary, numerical_list = numerical_summarize(numerical_cols, cutting_points)
    series_list = categorical_list + numerical_list
    distribution_summary = pd.concat(series_list)
    distribution_summary['distribution'] = distribution_summary['distribution'].astype('float64')
    if config:
        df1 = distribution_summary.set_index('feature_name').loc[config['category']]
    else:
        df1 = distribution_summary.set_index('feature_name').loc[
            list(df.select_dtypes(include=['category', 'object']).columns)]
    ca_df = df1.dropna().groupby('feature_name').apply(get_most_value)
    categorical_summary = pd.concat([categorical_summary, ca_df], axis=1, sort=True)
    distribution_summary.fillna('nan', inplace=True)

    to_excel(output_path, bool_summary, categorical_summary, numerical_summary, distribution_summary)


def to_excel(output_path, bool_summary, categorical_summary, numerical_summary, distribution_summary):
    writer = pd.ExcelWriter(output_path)
    bool_summary.to_excel(writer, '布尔特征')
    categorical_summary.to_excel(writer, '类型特征')
    numerical_summary.to_excel(writer, '数值特征')
    distribution_summary.to_excel(writer, '特征分布', index=False)
    summary_dict = {'布尔特征': [len(bool_summary), [2, 3, 4]], '类型特征': [len(categorical_summary), [2, 5, 7]],
                    '数值特征': [len(numerical_summary), [2]], '特征分布': [len(distribution_summary), [3]]}
    for summary in summary_dict.keys():
        worksheet = writer.sheets[summary]
        workbook = writer.book
        format1 = workbook.add_format({'num_format': '0.00%'})
        num_col = summary_dict[summary][1]
        num_row = summary_dict[summary][0]
        excel_range = get_excel_range(num_col, num_row)
        for k, j in excel_range:
            if j % 2 == 0:
                worksheet.conditional_format(k, {
                    'type': 'data_bar',
                    'data_bar_2010': True,
                    'bar_color': '#0066CC',
                    'value': 10,
                })
                worksheet.set_column(k, None, format1)

            else:
                worksheet.conditional_format(k, {
                    'type': 'data_bar',
                    'data_bar_2010': True,
                    'bar_color': '#008080',
                })
                worksheet.set_column(k, None, format1)
    writer.save()


def get_excel_range(n_col, n_row):
    excel_range = []
    for x in n_col:
        # range(2, n_col + 2):
        lis = []
        while x > 0:
            remainder = x % 26
            quote = x // 26
            if remainder == 0:
                remainder = 26
                quote -= 1
            lis.append(Const.num_to_alphabet[str(remainder)])
            x = quote

        name = ''.join(lis[::-1])
        excel_range.append(name + '2:' + name + str(n_row + 2))

    return list(zip(excel_range, range(0, len(n_col))))


def report_generate():
    pass


if __name__ == "__main__":
    data = DataFrame(
        [
            (1, True, 'X'),
            (3, False, 'Y'),
            (4, True, 'Z'),
            (3, False, 'M'),
        ],
        columns=['A', 'B', 'C']
    )
    config = {
        'booleans': [
            '12', '13', '14', '15', '16', '17', '141', '144', '145', 'pe_label'
        ],
        'category': [
            '146', '147', 'gender', 'in_hospital_season'
        ],
        'cutting_points': {
            '体重': [(0, 40.0), (40.0, 50.0), (50.0, 60.0), (60.0, 70.0), (70.0, 80.0), (80.0, 90.0),
                   (90.0, float("inf"))],
            '身高': [(0, 150.0), (150.0, 160.0), (170.0, 180.0), (180.0, 190.0), (190.0, 200.0), (200.0, float("inf"))],
            'bmi': [(0, 18.5), (18.5, 25.0), (25.0, 35.0), (30.0, 35.0), (35.0, 40.0), (40.0, float("inf"))]
        }
    }
    config_1 = {}
    df = pd.read_pickle('df_analysis.pkl')
    # df = pd.read_csv('240_data_with_pe_label.csv')
    summarize(df, 'analysis_result.xlsx')
