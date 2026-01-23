##  :macau: :round_pushpin:   MOPubBus Datasets 2025

 
### Data Segmentation
The file names of datasets indicate the segmentation of Macao bus data which are described in the following table.

| File name (structure)                    | File type | Bus Route | Season|
| :--                                  | :-:       |  :-:      | :-:   |
| **arrival_records\_{BusRoute}\_d0_{Season}_{revision (internal)}**   | .csv      |  {BusRoute}        | {Season} |
| 3_grandprix_2025_data   | .csv      |  3        | :racing_car: :macau:  |
| 3_normal_2025_data      | .csv      |  3        | :bus:        |
| 15_grandprix_2025_data     | .csv      |  15       | :racing_car: :macau: |
| 15_normal_2025_data        | .csv      |  15       | :bus:        |
| AP1_normal_2025_data       | .csv      |  AP1      | :bus:        |
|    :black_small_square:   :black_small_square:   :black_small_square:    |


:racing_car: :macau:  **:** Macau Grand Prix days,  
:bus:   **:**  Normal days.

:pushpin:   The rest of files  :page_with_curl:  in the Datasets  :file_folder:   have the same file name structure.



### Macao Public Bus Data Description 
The decription for Macao public bus data has been provided. Two statistical analysises inclduing PCA (principal component analysis) and correlation heatmap are available.   

:heavy_check_mark:  **:** The statisical analysis has been completed and the related source codes  :computer:   are available.

:computer: **:** Download [Phyton source codes](https://github.com/amangkim/MOPubBus/tree/main/sourcecodes)



| Feature        | Name          | Unit        |          Description                                                                 |
| :-:            | :-:           | :-:         | :--                                                                                  |
| *startStation* | Start station | --   | Indicates the departure station of the bus within the interval recorded by this data entry. |
| *endStation*   | End station   | --   | Represents the arrival station of the bus within the interval recorded by this data entry.  |
| *time*         | Arrival time stamp | _hh:mm:ss_   | Arrival time when a bus arrives the end station (i.e., arrival bus stop).      |
| *weekday*      | Week day      |0 ~ 6  | Encodes the day of the week as integers from 0 to 6, where 0 represents Monday and 6 represents Sunday.  |
| *passenger- Flow*| Passenger flow | -1, 0 ~ 5 | Provides an indication of passenger load condition inside the bus. Values range from -1 to 5, where -1 means no data available, and 0 to 5 represent increasing levels of crowding, with 5 being the most crowded.      
| *traffic- Condition*   | Traffic condition      | -1, 1 ~ 3  | Describes the traffic conditions on the road section between the startStation and endStation. Possible values are -1, 1, 2, 3, where -1 indicates no data available, 
| *busPlate*      | Bus plate      | **XX000** | Identifies the bus by its license plate number, which is unique to each vehicle.  |
| *weather*   | Weather condition      | 0, 1 ~ 5  | The weather feature encodes prevailing atmospheric conditions using integers from 0 to 5, where 1 denotes Clear, 2 denotes Clouds, 3 denotes Drizzle, 4 denotes Rain, and 5 denotes Thunderstorm. The value 0 is assigned to other unspecified weather conditions that cannot be classified into categories 1 through 5.|
| *arrival- Duration*  | Arrival duration    | Second  | Represents the duration it takes for the bus to travel the interval from _startStation_ to _endStation_.  |


### Revision History
```
2025.06.12: The first update of Readme.md file.

```
