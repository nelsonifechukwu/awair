/*
 * gps.c
 *
 *  Created on: Dec 18, 2023
 *      Author: ikpe Emmanuel
 *
 *  Contact information
 *  -------------------
 *
 * e-mail   :  echijiokeice@gmail.com
 */

/*
 * |---------------------------------------------------------------------------------
 * | Copyright (C) Ikpe Emmanuel,2019
 * |
 * | This program is free software: you can redistribute it and/or modify
 * | it under the terms of the GNU General Public License as published by
 * | the Free Software Foundation, either version 3 of the License, or
 * | any later version.
 * |
 * | This program is distributed in the hope that it will be useful,
 * | but WITHOUT ANY WARRANTY; without even the implied warranty of
 * | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * | GNU General Public License for more details.
 * |
 * | You should have received a copy of the GNU General Public License
 * | along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * |---------------------------------------------------------------------------------
 */

#include <Arduino.h>
#include <stdio.h>
#include <string.h>
#include "gps.h"



const char* GPS_HEAD[] = {
    "$GPRMC",
    "$GPGGA",
    "$GPGLL",
    "$GPGSA",
    "$GPGSV",
    "$GPVTG",
    "$GPZDA"
};

static int validate_gps_str(char* str) {
    char tmp[8] = { 0 };
    int i = 0;
    while (str[i] != ',') {
        tmp[i] = str[i];
        i++;
    }
    tmp[i] = '\0';
    for (int x = 0; x < 7; x++) {
        if (!strcmp(GPS_HEAD[x], tmp))
            return (x+1);
    }
    return -1;
}


static int GPS_parse(char* gps_str, GPS_Data *gps, int head) {
    int valid = validate_gps_str(gps_str);
    //Serial.println(valid);
    	if (valid == (head)) {
    	//Serial.println(gps_str);
        int start_index = (int)strlen(GPS_HEAD[valid]);
        int x = 0;
        int y = 0;
        int len = strlen(gps_str);
        while (len>0) {
          //Serial.print(gps_str[start_index]);
            if (gps_str[start_index] == '*')
                return valid;
            if (gps_str[start_index] == ',') {
                //skip to next character
                y = 0;
                x += 1;
                start_index++;
                continue;
            }
            if (x == 1) {
                gps->time[y] = gps_str[start_index];
                y++;
            }
            if (x == 2) {
                gps->status = gps_str[start_index];
                y++;
            }
            if (x == 3) {
                gps->_lat[y] = gps_str[start_index];
                y++;
            }
            if (x == 4) {
                gps->direction_NS = gps_str[start_index];
                y++;
            }
            if (x == 5) {
                gps->_long[y] = gps_str[start_index];
                y++;
            }
            if (x == 6) {
                gps->direction_EW = gps_str[start_index];
                y++;
            }
            if (x == 7) {
                gps->speed[y] = gps_str[start_index];
                y++;
            }
            if (x == 8) {
                gps->angle[y] = gps_str[start_index];
                y++;
            }
            if (x == 9) {
                gps->date[y] = gps_str[start_index];
                y++;
            }
            start_index++;
            len--;
        }
    }
    else  {
        return false;
        }
    return false;
}

int Process_GPS_Data(char gps_c, GPS_Data* gps, int head) {
    static int index1 = { 0 };
    static char buffer[140];
    static bool begin;
    if(gps_c == '$')begin = true;
    if(gps_c == '\r'){
        begin = false;
        buffer[index1] = '\0';
        int rt = GPS_parse(buffer, gps,head);
        memset(buffer,'\0',140);
        index1 = 0;
        return rt;
    }

    if(begin){
        buffer[index1] = gps_c; 
        index1++;
    }
    return 0;
}

