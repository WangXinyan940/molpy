#include "array.h"
#include <gtest/gtest.h>

TEST(testArray2, default_construct)
{
    Array2<int> arr({5, 3});
    EXPECT_EQ(5, arr.shape[0]);
    EXPECT_EQ(3, arr.shape[1]);
    EXPECT_EQ(15, arr.size());

}

TEST(testArray2, append)
{
    Array2<int> arr({5, 3});
    arr.replace(0, {1,2,3});
    arr.replace(1, {4,5,6});
    EXPECT_EQ(1, arr[0][0]);
    EXPECT_EQ(2, arr[0][1]);
    EXPECT_EQ(4, arr[1][0]);
}