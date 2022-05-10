#include "array.h"
#include <gtest/gtest.h>

TEST(testArray2, default_construct)
{
    Array2<int> arr(3);
    arr.append({1,2,3});
    arr.append({4,5,6});

    EXPECT_EQ(2, arr.get_nrows());
    EXPECT_EQ(3, arr.get_ncols());

}

TEST(testArray2, init_construct)
{
    Array2<int> arr(3, 3);
    EXPECT_EQ(3, arr.get_nrows());
    EXPECT_EQ(3, arr.get_ncols());

}


