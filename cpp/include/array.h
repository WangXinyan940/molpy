// #ifndef ARRAY_H
// #define ARRAY_H

// #include <vector>

// // template<typename T>
// // class Array {

// //     public:

// //         int nrows, ncols;

// //         void append(T value) {
// //             for (int i = 0; i < this->shape[1]; i++) {
// //                 this->data.emplace_back(value);
// //             }
// //         };

// //         void append(std::initializer_list<T> value) {
// //             for (auto i: value)
// //                 this->data.emplace_back(i);
// //         };

// //         ssize_t size() {
// //             return this->data.size();
// //         };

// //         std::vector<T> operator[](int index) {
// //             std::vector<T> tmp;
// //             for (int i = 0; i < this->shape[1]; i++) {
// //                 tmp.emplace_back(this->data[index*this->shape[1]+i]);
// //             }
// //             return tmp;
// //         };

// //         void replace(int index, std::initializer_list<T> value) {
// //             int i = 0;
// //             for (auto elem : value) {
// //                 this->data[index*this->shape[1]+i] = elem;
// //                 i++;
// //             }
// //         }

// //         std::vector<int> shape;

// //         T* getData() {
// //             return this->data.data();
// //         }

// //     private:
// //         int nrows, ncols;
// //         std::vector<T> data;

// // };



// #endif ARRAY_H // ARRAY_H

#ifndef ARRAY_H
#define ARRAY_H

#include <vector>
#include <ostream>

template<typename T>
class Array {

    public:

        std::vector<T> data;
        std::vector<int> shape;
        std::vector<int> strides;
        int ndim;

        void append(T value) {
            this->data.emplace_back(value);
        }

        void append(std::initializer_list<T> value) {
            for (auto i: value)
                this->data.emplace_back(i);
        }

        T* ptr() {
            return this->data.data();
        }

        void clear() {
            this->data.clear();
        }

        T dtype() {
            return data.value_type;
        }

};

#endif // ARRAY_H