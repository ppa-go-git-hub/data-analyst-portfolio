import pandas as pd
import os

def model(dbt, session):
    filepath = dbt.config.get('filepath')
    year_min = dbt.config.get('year_min', None)
    year_max = dbt.config.get('year_max', None)
    if filepath.startswith('~'):
        home_directory = session.sql("SELECT current_setting('home_directory') AS home_directory").df().iloc[0,0]
        filepath = os.path.join(home_directory, filepath[1:].lstrip(os.sep))
    return parse_insee_xlsx(filepath, year_min=year_min, year_max=year_max)

def parse_insee_xlsx(filepath, *, year_min=None, year_max=None):
    assert year_min is None or year_max is None or year_min <= year_max
    with pd.ExcelFile(filepath) as excel_file:
        years = [
            year
            for year in map(int, filter(str.isdigit, excel_file.sheet_names))
            if year_min is None or year >= year_min
            if year_max is None or year <= year_max
        ]
        dfs = [ df for year in years for df in parse_insee_xlsx_tab(excel_file, year) ]
    return pd.concat(
        (
            df.melt(
                id_vars=['year','gender','region'],
                var_name='age_group',
                value_name='total',
                ignore_index=True,
            )[['year','gender','age_group','region','total']]
            for df in dfs
        ),
        ignore_index=True,
    )

def parse_insee_xlsx_tab(excel_file, year):
    if year < 1999:
        raise NotImplementedError('parse_insee_xlsx_tab(): not implemented for year < 1999')
    df = pd.read_excel(excel_file, sheet_name=f'{year}', header=None, dtype=object)
    assert df.shape[0] >= 7 # Above (3) / Header (2) / Below (2)
    assert df.shape[1] >= 7 # Region (1) / All (2) / Male (2) / Female (2)
    assert (df.shape[1] - 1) % 3 == 0
    n = (df.shape[1] - 1) // 3
    assert df.iloc[0,0] == "Estimation de population au 1er janvier, par région, sexe et âge quinquennal"
    assert df.iloc[1,0] == f"Année {year}"
    assert df.iloc[2,:].isna().all()
    assert df.iloc[3,0] == "Régions"
    assert (df.iloc[3,1:][ df.iloc[3,1:].notna() ] == [ "Ensemble", "Hommes", "Femmes" ]).all()
    assert (df.iloc[3,1:][ df.iloc[3,1:].notna() ].index == range(1, df.shape[1], n)).all()
    assert df.iloc[4,0:1].isna().all()
    assert df.iloc[-1,0].startswith("Source : Insee - Estimations de population")
    assert df.iloc[-2,:].isna().all()
    assert df.iloc[5:-2,:].notna().all().all()
    df_all = df.iloc[5:-2,0*n+1:1*n+1].astype(int)
    df_m   = df.iloc[5:-2,1*n+1:2*n+1].astype(int)
    df_f   = df.iloc[5:-2,2*n+1:3*n+1].astype(int)
    assert df_all.notna().all().all()
    assert df_m  .notna().all().all()
    assert df_f  .notna().all().all()
    assert (df_all >= 0).all().all()
    assert (df_m   >= 0).all().all()
    assert (df_f   >= 0).all().all()
    df_all.columns = df.iloc[4,0*n+1:1*n+1]
    df_m  .columns = df.iloc[4,1*n+1:2*n+1]
    df_f  .columns = df.iloc[4,2*n+1:3*n+1]
    df_all.columns.name = 'age_group'
    df_m  .columns.name = 'age_group'
    df_f  .columns.name = 'age_group'
    assert (df_all.columns == df_m.columns).all()
    assert (df_all.columns == df_f.columns).all()
    assert (df_all == df_m + df_f).all().all()
    assert df_m.columns[-1] == "Total"
    assert df_f.columns[-1] == "Total"
    assert (df_m.iloc[:,:-1].sum(axis=1) == df_m.iloc[:,-1]).all()
    assert (df_f.iloc[:,:-1].sum(axis=1) == df_f.iloc[:,-1]).all()
    del df_m['Total']
    del df_f['Total']
    df_m['year'] = year
    df_f['year'] = year
    df_m['gender'] = "Hommes"
    df_f['gender'] = "Femmes"
    df_m['region'] = df.iloc[5:-2,0]
    df_f['region'] = df.iloc[5:-2,0]
    return df_m, df_f

def main():
    while True:
        xlsx_input_filename = input('XLSX input file ? ')
        if xlsx_input_filename.endswith('.xlsx'):
            break
        else:
            print('Illegal filename extension (expected: .xlsx)')
    while True:
        line = input('Year min (empty = no minimum) ? ')
        if len(line) == 0:
            year_min = None
            break
        elif not(line.isdigit() and line[0] != '0'):
            print('Illegal value (expected: empty or positive integer)')
        else:
            year_min = int(line)
            break
    while True:
        line = input('Year max (empty = no maximum) ? ')
        if len(line) == 0:
            year_max = None
            break
        elif not(line.isdigit() and line[0] != '0'):
            print('Illegal value (expected: empty or positive integer)')
        else:
            year_max = int(line)
            if year_min is None or year_min <= year_max:
                break
            else:
                print(f'Ill-formed year range: min={year_min} > max={year_max}')
    while True:
        csv_output_filename = input('CSV output file ? ')
        if csv_output_filename.endswith('.csv'):
            break
        else:
            print('Illegal filename extension (expected: .csv)')
    print('Reading raw data from:', xlsx_input_filename)
    print(f'Year range: min={year_min}, max={year_max}')
    df = parse_insee_xlsx(xlsx_input_filename, year_min=year_min, year_max=year_max)
    print('Writing processed data to:', csv_output_filename)
    df.to_csv(csv_output_filename, index=False)
    print('Done')

if __name__ == '__main__':
    main()
