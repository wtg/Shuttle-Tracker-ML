#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <vector>
#include <tuple>
#include <sstream>
#include "bus.h"

// pase time into date, hour, min, sec
std::vector<std::string> parse_time(std::string time) {
    std::string word;
    std::vector<std::string> temp_result;
    std::vector<std::string> result;
    std::stringstream temp1(time);
    while (std::getline(temp1, word, ' ')) {
        temp_result.push_back(word);
    }
    result.push_back(temp_result[0]);

    std::stringstream temp2(temp_result[1]);
    while (std::getline(temp2, word, ':')) {
        result.push_back(word);
    }
    result.push_back(temp_result[2]);

    return result;
}

// construc time & location
Time_loc::Time_loc(std::string longitude, std::string latitude, std::vector<std::string> time_info) {
    add_location(longitude, latitude);

    date = time_info[0];
    hour = std::stoi(time_info[1]);
    min_start = std::stoi(time_info[2]);
    min_finish = min_start + 10;
    addition = time_info[3];
}

// if later than time_loc return true; else return false
bool Time_loc::compare(std::vector<std::string> time_sum) {
    int test_hour = std::stoi(time_sum[1]);
    int test_min = std::stoi(time_sum[2]);

    if (date < time_sum[1]) {
        return true;
    }

    if (hour < test_hour) {
        return true;
    }

    if (min_finish < test_min) {
        return true;
    }

    return false;
}

// add location
void Time_loc::add_location(std::string longitude, std::string latitude) {
    double a = std::stod(longitude);
    double b = std::stod(latitude);
    locations.push_back(std::make_tuple(a, b));
}

// check if is within 10 min
bool Time_loc::in_range(std::vector<std::string> time_info) {
    int test_hour = std::stoi(time_info[1]);
    int test_min = std::stoi(time_info[2]);
    if (date != time_info[1]) {
        return false;
    }

    if (hour != test_hour) {
        return false;
    } 

    if ((test_min < min_start) || (min_finish < test_min)) {
        return false;
    }

    return true;
}

// print out locations
void Time_loc::print_locations() {
    int i;
    for (const auto& i : locations) {
        std::cout << "( " << std::get<0>(i) << ", " << std::get<1>(i) << ") " << std::endl;
    }
    std::cout << std::endl;
} 

// print the entire thing
void Time_loc::print_loc() {
    std::cout << "date: " << date << ", hour: " << hour << ", minute: " << min_start << std::endl;
    print_locations();
    std::cout << std::endl;
}

// construct bus
Bus::Bus(std::vector<std::string> bus_info) {
    ID = bus_info[0];
    std::vector<std::string> time_sum = parse_time(bus_info[3]);
    times.push_back(Time_loc(bus_info[1], bus_info[2], time_sum));
}

// insert times
void Bus::insert_time(std::vector<std::string> time_sum, Time_loc temp_timeLoc) {
    int i;
    std::list<Time_loc>::iterator it;
    for (it = times.begin(); it != times.end(); it++) {
        if ((*it).compare(time_sum)) {
            times.insert(it, temp_timeLoc);
        }
    }
}

// search through times, if exist time <= 10min, add to location; else, add to time
void Bus::add(std::vector<std::string> bus_info) {
    std::cout << "bus id: " << ID << std::endl;
 
    int i;
    int len = times.size();
    bool is_inRange = false;
    std::vector<std::string> time_sum = parse_time(bus_info[3]);
    
    // check if is in the time range: if yes, add location; if no, push back new time_loc
    std::list<Time_loc>::iterator it;
    for (it = times.begin(); it != times.end(); it++) {
        if ((*it).in_range(time_sum)) {
            is_inRange = true;
            (*it).add_location(bus_info[1], bus_info[2]);
        }
    }

    if (is_inRange == false) {
        Time_loc temp_timeLoc(bus_info[1], bus_info[2], time_sum);
        insert_time(time_sum, temp_timeLoc);
    }
}

// print times
void Bus::print_times() {
    std::cout << "times.size is " << times.size() << std::endl;
    std::list<Time_loc>::iterator it;
    for (it = times.begin(); it != times.end(); it++) {
        (*it).print_loc();
    }
}
