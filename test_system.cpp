// ! c++
// Test system cpp
// Copyright by @Truongchinh304

#include <bits/stdc++.h>
#include <cstdlib> // random
#include <unistd.h> // time delay (sleep)
#define __TruongChinh__ signed main()
#define loop while (true)
#define ll long long
#define pb push_back
#define FOR(i, a, b) for(int i = a; i <= b; i++)
#define REP(i, n) for(int i = 0; i < n; i++)
#define SNT(i, a, n) for(int i = 2; i*i <= n; i++)
#define fast_io ios::sync_with_stdio(0); cin.tie(0);
#define TIME (1.0 * clock() / CLOCKS_PER_SEC)
using namespace std;

int ktra_snt(int n){
    SNT(i, 2, n){
        if(n % i == 0) return 0;
    }
    return n > 1;
}

void random_snn(int n, vector<int>& mang){
    srand(time(0));
    REP(i, n){
        int snn = rand()%99 + 1;
        mang.pb(snn);
    }
}

__TruongChinh__ {
    fast_io;

    int gioi_han; cin >> gioi_han;
    vector<int> cac_so_nt;
    vector<int> cac_so_knt;
    cout << "Bang so nguyen to" << endl;
    //REP(i, gioi_han){
    while(gioi_han --){
        if(ktra_snt(gioi_han)){
            cout << gioi_han << " ";
            cac_so_nt.pb(gioi_han);
        } else {
            cout << "X ";
            cac_so_knt.pb(gioi_han);
        }    
    }
    cout << "\nCac so nguyen to gom: " << endl;
    for(int x : cac_so_nt){
        cout << x << " ";
    }
    cout << "\nCac so khong nguyen to gom: " << endl;
    for(int x : cac_so_knt){
        cout << x << " ";
    }
    vector<int> snt_td = cac_so_nt ;
    sort(snt_td.begin(), snt_td.end()); //, greater<int>());
    cout << "\nSo nguyen to tang dan: " << endl;
    for(int x : snt_td){
        cout << x << " "; 
    } 

    cerr << "Time: " << TIME << " s.\n";
    return 0;
}   
