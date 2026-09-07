# import pandas as pd

# def sort_by_day_plate_time(file_path, mapping_file_path, output_path):
#     """
#     Sort data by full_day, busPlate, and datetime,
#     and map station codes to station numbers
#     """
#     # Read main data file
#     df = pd.read_csv(file_path)

#     # Read mapping file
#     mapping_df = pd.read_csv(mapping_file_path)

#     # Create mapping dictionary: staCode -> staNum
#     station_mapping = dict(zip(mapping_df['staCode'], mapping_df['staNum']))

#     # Map stations
#     df['startStation'] = df['startStation'].map(station_mapping)
#     df['endStation'] = df['endStation'].map(station_mapping)

#     # Combine date and time into datetime
#     df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

#     # Sort by full_day, busPlate, and datetime
#     df_sorted = df.sort_values(
#         by=['date', 'busPlate', 'datetime'],
#         ascending=[True, True, True]
#     )

#     # Drop temporary datetime column
#     df_sorted = df_sorted.drop(columns=['datetime'])

#     # Save to output path
#     df_sorted.to_csv(output_path, index=False)

#     return df_sorted


# def main():
#     # Input paths
#     data_file_path = ('D:/School/MPU_Master/2025Busdata/data(remove outliers date_grandprix13-16)/AP1_normal_data_filtered.csv')
#     mapping_file_path = ('D:/School/MPU_Master/BusData/route_stop_lists/stops_list_normal_AP1.csv')

#     # Output path
#     output_path = ('D:/School/MPU_Master/2025Busdata/System/sorted_mapped_bus_data_AP1_normal.csv')

#     sorted_df = sort_by_day_plate_time(
#         data_file_path,
#         mapping_file_path,
#         output_path
#     )

#     print("Sorted and mapped data preview:")
#     print(sorted_df.head())


# if __name__ == "__main__":
#     main()


# # import pandas as pd

# # def sort_by_day_plate_time(file_path, mapping_file_path, output_path):
# #     """
# #     Sort data by date, busPlate, and datetime,
# #     map station codes to station numbers,
# #     and REMOVE rows that failed mapping
# #     """
# #     # --------------------------------------------------
# #     # Load data
# #     # --------------------------------------------------
# #     df = pd.read_csv(file_path)
# #     mapping_df = pd.read_csv(mapping_file_path)

# #     # --------------------------------------------------
# #     # Build mapping dictionary
# #     # --------------------------------------------------
# #     station_mapping = dict(
# #         zip(mapping_df['staCode'], mapping_df['staNum'])
# #     )

# #     # --------------------------------------------------
# #     # Map station codes
# #     # --------------------------------------------------
# #     df['startStation'] = df['startStation'].map(station_mapping)
# #     df['endStation'] = df['endStation'].map(station_mapping)

# #     # --------------------------------------------------
# #     # Remove rows that failed mapping
# #     # --------------------------------------------------
# #     df = df.dropna(subset=['startStation', 'endStation'])

# #     # --------------------------------------------------
# #     # Combine date & time
# #     # --------------------------------------------------
# #     df['datetime'] = pd.to_datetime(
# #         df['date'] + ' ' + df['time'],
# #         errors='coerce'
# #     )

# #     # --------------------------------------------------
# #     # Sort
# #     # --------------------------------------------------
# #     df_sorted = df.sort_values(
# #         by=['date', 'busPlate', 'datetime'],
# #         ascending=[True, True, True]
# #     )

# #     # --------------------------------------------------
# #     # Cleanup
# #     # --------------------------------------------------
# #     df_sorted = df_sorted.drop(columns=['datetime'])

# #     # --------------------------------------------------
# #     # Save
# #     # --------------------------------------------------
# #     df_sorted.to_csv(output_path, index=False)

# #     return df_sorted


# # def main():
# #     data_file_path = (
# #         'D:/School/MPU_Master/2025Busdata/data(remove outliers date_grandprix13-16)/'
# #         '3_d0_grandprix_data_filtered.csv'
# #     )

# #     mapping_file_path = (
# #         'D:/School/MPU_Master/BusData/route_stop_lists/'
# #         'stops_list_grandprix_3d0.csv'
# #     )

# #     output_path = (
# #         'D:/School/MPU_Master/2025Busdata/System/'
# #         'sorted_mapped_bus_data_3_grandprix.csv'
# #     )

# #     sorted_df = sort_by_day_plate_time(
# #         data_file_path,
# #         mapping_file_path,
# #         output_path
# #     )

# #     print("Final dataset size:", len(sorted_df))
# #     print(sorted_df.head())


# # if __name__ == "__main__":
# #     main()


import pandas as pd

def sort_by_day_plate_time(file_path, mapping_file_path, output_path):
    """
    Sort data by date, busPlate, and datetime,
    and map station codes to station numbers with context-aware correction
    """

    # ==============================
    # 1. Read data
    # ==============================
    df = pd.read_csv(file_path)
    mapping_df = pd.read_csv(mapping_file_path)

    # ==============================
    # 2. Preserve raw station codes
    # ==============================
    df['startStation_raw'] = df['startStation']
    df['endStation_raw'] = df['endStation']

    # ==============================
    # 3. Basic mapping (staCode -> staNum)
    # ==============================
    station_mapping = dict(zip(mapping_df['staCode'], mapping_df['staNum']))

    df['startStation'] = df['startStation'].map(station_mapping)
    df['endStation'] = df['endStation'].map(station_mapping)

    # ==============================
    # 4. Context-aware correction (核心)
    # ==============================
    def fix_station(row):
        start = row['startStation_raw']
        end = row['endStation_raw']

        # ---------- M1/18 ----------
        if start == 'M1/18' and end == 'M222/2':
            row['startStation'] = 0
        if end == 'M1/18' and start == 'M247':
            row['endStation'] = 22

        # ---------- M254 ----------
        if start == 'M254' and end == 'T316':
            row['startStation'] = 6
        if end == 'M254' and start == 'M239/2':
            row['endStation'] = 6

        if start == 'M254' and end == 'M64':
            row['startStation'] = 18
        if end == 'M254' and start == 'M239/1':
            row['endStation'] = 18

        return row

    df = df.apply(fix_station, axis=1)

    # ==============================
    # 5. Create datetime for sorting
    # ==============================
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')

    # ==============================
    # 6. Sort data
    # ==============================
    df_sorted = df.sort_values(
        by=['date', 'busPlate', 'datetime'],
        ascending=[True, True, True]
    )

    # ==============================
    # 7. Clean up
    # ==============================
    df_sorted = df_sorted.drop(columns=['datetime', 'startStation_raw', 'endStation_raw'])

    # ==============================
    # 8. Save output
    # ==============================
    df_sorted.to_csv(output_path, index=False)

    return df_sorted


def main():
    # ==============================
    # Input paths
    # ==============================
    data_file_path = 'D:/School/MPU_Master/2025Busdata/data(remove outliers date_grandprix13-16)/AP1_grandprix_data_filtered.csv'
    mapping_file_path = 'D:/School/MPU_Master/BusData/route_stop_lists/stops_list_normal_AP1.csv'

    # ==============================
    # Output path
    # ==============================
    output_path = 'D:/School/MPU_Master/2025Busdata/System/sorted_mapped_bus_data_AP1_grandprix.csv'

    # ==============================
    # Run processing
    # ==============================
    sorted_df = sort_by_day_plate_time(
        data_file_path,
        mapping_file_path,
        output_path
    )

    print("Sorted and mapped data preview:")
    print(sorted_df.head())


if __name__ == "__main__":
    main()

