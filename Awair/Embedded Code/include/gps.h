/*
 * gps.h
 *
 *  Created on: Nov 15, 2019
 *      Author: Bulanov Konstantin
 */
#ifndef _GPS_H
#define _GPS_H




enum GPS_head {
    GPRMC=1,
    GPGGA,
    GPGLL,
    GPGSA,
    GPGSV,
    GPVTG,
    GPZDA
};




typedef struct GPS_data {
    char time[15];
    char status;
    char direction_NS;
    char direction_EW;
    char speed[15];
    char angle[15];
    char date[15];
    char _lat[15];
    char _long[15];
}GPS_Data;

int Process_GPS_Data(char gps_c, GPS_Data* gps, int head);

#endif

