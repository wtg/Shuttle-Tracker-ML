#ifndef BUS_H
#define BUS_H
#include <iostream>
#include <stdlib.h>
#include <sstream>
#include <stdio.h>
#include <string>
#include <vector>
#include <list>
#include <tuple>

// store time and location with in 10 min
class Time_loc {
public:
    Time_loc(std::string a, std::string b, std::vector<std::string> time_info);

    int getHour() {return hour;}
    int getStart_min() {return min_start;}
    int getFinishe_min() {return min_finish;}
    void print_loc();
    void print_locations();

    bool compare(std::vector<std::string> time_sum);
    bool in_range(std::vector<std::string> time_info);
    void add_location(std::string longitude, std::string latitude);

private:
    friend class Bus;
    std::string date;
    int hour;
    int min_start;
    int min_finish;
    std::string addition;

    std::vector<std::tuple<double, double>> locations;
 
};

// store bus information
class Bus {
    public:
        Bus(std::vector<std::string> bus_info);

        const std::string getID() {return ID;} 

        void add(std::vector<std::string> bus_info);
        void insert_time(std::vector<std::string> time_sum, Time_loc temp_timeLoc);
        void print_times();

    private:
        std::string ID;
        std::list<Time_loc> times;
        int find_index(std::vector<std::string>time_sum);

};

std::vector<std::string> parse_time(std::string time);

#endif