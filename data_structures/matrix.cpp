#include "lib.hpp"
#include <vector>

using namespace std;

class Matrix {
public:
    int rows_;
    int cols_;
    int n_;
    std::vector<double> data_;

    Matrix(int r, int c, double val = 0)
    : rows_(r), cols_(c), n_(r * c), data_(r * c, val) {}

    inline double& operator[](int r, int c) {
        return data_[r * cols_ + c];
    }

    inline const double& operator[](int r, int c) const {
        return data_[r * cols_ + c];
    }

    Matrix operator*(const Matrix& other) const {
    //cache friendly version
        assert(cols_ == other.rows_);

        Matrix result(rows_, other.cols_);

        for(int i = 0; i < rows_; ++i)
        for(int k = 0; k < cols_; ++k)
        for(int j = 0; j < other.cols_; ++j)
        {
            result[i, j] += (*this)[i, k] * other[k, j];
        }

        return result;
    }

    // Matrix operator*(const Matrix& other) const {
    //     assert(cols_ == other.rows_);

    //     Matrix result(rows_, other.cols_);

    //     for(int i = 0; i < rows_; ++i)
    //     for(int j = 0; j < other.cols_; ++j)
    //     for(int k = 0; k < cols_; ++k)
    //     {
    //         result[i, j] += (*this)[i, k] * other[k, j];
    //     }

    //     return result;
    // }

    void print(int max_cols = 10, int max_rows = 10){
        for(int r = 0; r < min(rows_, max_rows); ++r) {
            for(int c = 0; c < min(cols_, max_cols); ++c)
                cout << (*this)[r, c] << " ";
            if (cols_ > max_cols) {
                cout << "...";
            }
            cout << "\n";
        }
        if (rows_ > max_rows) {
            cout << "...\n";
        }
    }
};

Matrix generate_matrix(unsigned r = 10, unsigned c = 10, int val_from = 0, int val_to = 100) {
    Matrix A(r, c);
    for(int i = 0; i < r; ++i)
        for(int j = 0; j < c; ++j)
            A[i, j] = random_int(val_from, val_to);
    return A;
}

int main() {
    Matrix A = generate_matrix(1000, 1000);
    Matrix B = generate_matrix(1000, 1000);
    timming("multiple 2 matrix", [&A, &B](){
        Matrix C = A * B;
    });
}
