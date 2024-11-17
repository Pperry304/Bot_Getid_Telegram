// ! c++
// Mảng 3 chiều
// Copyright by @Truongchinh304

#include <bits/stdc++.h>
#define defi int 
#define defv void
#define __TruongChinh__ signed main()
using namespace std;

defi kiem_tra_so_nguyen_to(int n){
    for(int i = 2; i <= sqrt(n); i++){
        if(n % i == 0){
            return 0;
        }
    }
    return n > 1;
}

defv nhap_mang_3_chieu(int mang_3_chieu[][50][50], int n, int m, int p){
    int tong_phan_tu_trong_mang = 0;
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= m; j++){
            for(int k = 1; k <= p; k++){ 
                cout << "Nhập phần tử " << "[" << i << "]" << "[" << j << "]" << "[" << k << "]: ";
                cin >> mang_3_chieu[i][j][k]; 
                tong_phan_tu_trong_mang += mang_3_chieu[i][j][k];
            }
        }
    }
    cout << "Tổng phần tử trong mảng là: " << tong_phan_tu_trong_mang << endl;
}

defv in_mang_3_chieu_so_nt(int mang_3_chieu[][50][50], int n, int m, int p){
    for(int i = 1; i <= n; i++){
        cout << "Mặt" << i << ":\n";
        vector<int> mang_chua_so_khong_nt;
        for(int j = 1; j <= m; j++){
            for(int k = 1; k <= p; k++){
                if(kiem_tra_so_nguyen_to(mang_3_chieu[i][j][k])){
                    cout << mang_3_chieu[i][j][k] << "  ";
                }
                else{
                    cout << "X" << "  ";
                    mang_chua_so_khong_nt.push_back(int(mang_3_chieu[i][j][k])); 
                }
            }
            cout << endl;
        }
        cout << "Các số không nguyên tố là: ";
        for(int i = 0; i < (mang_chua_so_khong_nt.size()); i++){
            cout << mang_chua_so_khong_nt[i] << " ";
        }
        cout << endl;
    }
    
}

__TruongChinh__ {
    cout << "Nhập số mặt, số dòng và số cột: ";
    int n, m, p; cin >> n >> m >> p;
    int mang_3_chieu[50][50][50];
    int mang_chua_so_khong_nt[50]; // Tạo mảng 1d chứa các số không nguyên tố 
    cout << "Nhập các phần tử mảng 3 chiều:\n";
    nhap_mang_3_chieu(mang_3_chieu, n, m, p);
    cout << "\nMảng số nguyên tố là:\n";
    in_mang_3_chieu_so_nt(mang_3_chieu, n, m, p);
}