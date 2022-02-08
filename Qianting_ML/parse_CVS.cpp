#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include "bus.h"

// print content
void print_contend(const std::vector<std::vector<std::string>> content) {
 	for(int i = 0; i < content.size(); i++) {
        
		for(int j = 0; j < content[i].size(); j++) {
			std::cout << content[i][j] << " ";
		}
		std::cout << "\n";
	
	}   
}

// print buses
void print_buses(std::vector<Bus> buses) {
    int i;
    for (int i = 0; i < buses.size(); i++) {
        std::cout << "bus id: " << buses[i].getID() << std::endl;
        buses[i].print_times();
        std::cout << std::endl;
    }

}

// read in the file and store in the content vector 
void read_file(std::vector<std::vector<std::string>>* content, std::string fname) {
    std::fstream file;
    std::string line, word;
    std::vector<std::string> row;
    file.open(fname, std::ios::in);
	if(!file.is_open()) {
        std::cout << "Could not open the file" << std::endl;
	}

    while(std::getline(file, line)) {
        row.clear();

        std::stringstream temp(line);
        while (std::getline(temp, word, ',')) {
            row.push_back(word);
        }

        (*content).push_back(row);
    }

    file.close();
}

// return index if contain id; else return -1
int contain(std::vector<Bus> buses, std::string id) {
    int i;
    for (i = 0; i < buses.size(); i++) {
        if (buses[i].getID() == id) {
            return i;
        }
    }

    return -1;
}

// store the buses in the class
std::vector<Bus> store_bus(std::vector<std::vector<std::string>> content) {
    int i;
    int j;
    int index;
    std::vector<Bus> result;

    for (i = 0; i < content.size(); i++) {
        index = contain(result, content[i][0]);
        if (index == -1) {
            Bus new_bus(content[i]);
            result.push_back(new_bus);
        }
        else {
            result[index].add(content[i]);
        }
    }

    return result;
}

int main(int argc, char **argv) {
    if (argc > 2) {
        exit(-1);
    }
    std::string fname;
	fname = argv[1];

    std::vector<std::vector<std::string>> content;
    read_file(&content, fname);

    std::vector<Bus> buses = store_bus(content);

    print_buses(buses);

    return 0;
}