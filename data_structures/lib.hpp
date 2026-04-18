#include <time.h>
#include <chrono>
#include <iostream>
#include <random>
#include <cassert>

using namespace std;

template<typename Func>
void timming(const string& task_name, Func func) {
    cout << "Running " << task_name << "..." << endl;
    auto t1 = chrono::high_resolution_clock::now();
    func();
    auto t2 = chrono::high_resolution_clock::now();
    double seconds = chrono::duration<double>(t2 - t1).count();
    cout << "Done "
        << chrono::duration_cast<chrono::milliseconds>(t2-t1).count()
        << " milliseconds" << endl;
}


template<typename INT>
inline INT random_int(INT from, INT to) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_int_distribution<INT> distrib(from, to);
    return distrib(gen);
}
