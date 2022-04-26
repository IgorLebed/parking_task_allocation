# Task allocation
## _Introduction_

[![I|Lebedev](/screenshots/icon_ras.png)](https://spcras.ru/units/employee.php?ID=462463)

## Features
* # Input topic:
    * ##### _Menu topic_
```sh
/car_input_menu std_msgs/Int64 "data: 0"
```
* 1 -- Leave the car in the parking lot
* 2 -- Pick up car from parking
* 3 --  Availables places list
* # Output topic:
    * ##### Allocation parking place
```sh
/parking_place std_msgs/Float64 "data: 0.0"
```

## Installation

Information about the library of the [Hungarian algorithm](https://software.clapper.org/munkres/)


Install the dependencies.

```sh
pip install munkres
```

## Work example

* # Menu
![menu_list](/screenshots/menu_list.jpg)

* # Add car in list
    * Add car on 1h to 6h
    ![parking1_6](/screenshots/parkin1_6.jpg)
    * Add car on 6h to 12h
    ![parking6_12](/screenshots/parkin6_12.jpg)
    * Add car on 12h to 18h
    ![parking12_18](/screenshots/parkin12_18.jpg)
    * Add car on 18h to 24h
    ![parking18_24](/screenshots/parkin18_24.jpg) 
* # Delete car from list
![pick_up_car](/screenshots/pick_up_1.jpg) 
