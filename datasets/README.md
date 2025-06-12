# MOPubBus Data Description
The decription for Macao public bus data provides in Table 1 (see the below table). Two statistical analysises inclduing PCA (principal component analysis) and correlation heatmap are available.   

:heavy_check_mark:  means the statisical analysis has been completed and the related source codes  :computer:   are available.

:computer: Download [Phyton source codes](https://github.com/amangkim/MOPubBus/tree/main/sourcecodes)



### Data Desciption (Table 1)

| Feature        | Name          | Unit        |          Description                                                                 |PCA | Heat- map |
| :-:            | :-:           | :-:         | :--                                                                                  | :-: | :-:      |
| *startStation* | Start station | --   | Indicates the departure station of the bus within the interval recorded by this data entry. | --  | -- |
| *endStation*   | End station   | --   | Represents the arrival station of the bus within the interval recorded by this data entry.  | :heavy_check_mark:  | -- |
| *time*         | Arrival time stamp | _hh:mm:ss_   | Arrival time when a bus arrives the end station (i.e., arrival bus stop).      | :heavy_check_mark:  | :heavy_check_mark:|
| *weekday*      | Week day      |0 ~ 6  | Encodes the day of the week as integers from 0 to 6, where 0 represents Monday and 6 represents Sunday.  | :heavy_check_mark:  | :heavy_check_mark:|
| *passenger- Flow*| Passenger flow | -1, 0 ~ 5 | Provides an indication of passenger load condition inside the bus. Values range from -1 to 5, where -1 means no data available, and 0 to 5 represent increasing levels of crowding, with 5 being the most crowded.      | :heavy_check_mark:  | :heavy_check_mark:|
| *traffic- Condition*   | Traffic condition      | -1, 1 ~ 3  | Describes the traffic conditions on the road section between the startStation and endStation. Possible values are -1, 1, 2, 3, where -1 indicates no data available, and 1 to 3 represent increasing levels of traffic congestion, with 3 indicating heavy traffic.  | :heavy_check_mark:  | :heavy_check_mark:|
| *busPlate*      | Bus plate      | **XX000** | Identifies the bus by its license plate number, which is unique to each vehicle.  | -- | -- |
| *arrival- Duration*  | Arrival duration    | Second  | Represents the duration it takes for the bus to travel the interval from _startStation_ to _endStation_.  | :heavy_check_mark:  | :heavy_check_mark:|
