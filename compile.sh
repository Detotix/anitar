#!/bin/bash

echo -- compiling

if [[ "$1" == "-release" ]]; then
    g++ -std=c++17 -Os -s -flto -fdata-sections -ffunction-sections -c src/loudness.cpp -Iinclude -o loudness.o
    g++ -std=c++17 -Os -s -flto -fdata-sections -ffunction-sections -c src/main.cpp -Iinclude -o main.o
    g++ -std=c++17 -Os -s -flto -fdata-sections -ffunction-sections -c src/py.cpp -Iinclude -I/usr/include/python3.11 -o py.o
    g++ loudness.o main.o py.o -I/usr/include/python3.11 -o anitar.out -lportaudio -pthread -lpython3.11 -lsfml-graphics -lsfml-window -lsfml-system -O3 -march=native -mtune=native -ffast-math -fno-exceptions -fno-rtti -fomit-frame-pointer -Wl,--gc-sections -flto -s
else
    g++ -std=c++17 -c src/loudness.cpp -Iinclude -o loudness.o
    g++ -std=c++17 -c src/main.cpp -Iinclude -o main.o
    g++ -std=c++17 -c src/py.cpp -Iinclude -I/usr/include/python3.11 -o py.o
    g++ loudness.o main.o py.o -I/usr/include/python3.11 -o anitar.out -lportaudio -pthread -lpython3.11 -lsfml-graphics -lsfml-window -lsfml-system
    ./anitar.out
fi

echo -- cleanup
rm *.o

echo -- finished

